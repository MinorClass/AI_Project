import argparse, time, sys
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

def list_devices():
    print("== Audio Devices ==")
    for i, dev in enumerate(sd.query_devices()):
        io = []
        if dev["max_input_channels"] > 0: io.append("IN")
        if dev["max_output_channels"] > 0: io.append("OUT")
        print(f"[{i:2d}] ({'/'.join(io) or '-'}) {dev['name']}")

def pick_device(name_or_index):
    if name_or_index is None:
        return None
    # index가 들어오면 그대로
    try:
        return int(name_or_index)
    except:
        pass
    # 이름 일부 매칭
    name_lower = name_or_index.lower()
    for i, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] > 0 and name_lower in dev["name"].lower():
            return i
    raise RuntimeError(f"입력 장치 '{name_or_index}' 를 찾을 수 없습니다. --list-devices 로 확인하세요.")

def load_model(model_size: str, compute_type: str):
    print(f"[info] loading faster-whisper model='{model_size}', compute_type='{compute_type}' ...")
    return WhisperModel(model_size, compute_type=compute_type)

def transcribe_array(model, audio_f32, lang="ko"):
    segments, info = model.transcribe(audio_f32, language=lang, beam_size=5)
    text = "".join([seg.text for seg in segments]).strip()
    return text

def record_fixed_seconds(sec: float, device_idx=None, sr=16000):
    print(f"[rec] recording {sec:.1f}s @ {sr}Hz ... (Ctrl+C 중지)")
    audio = sd.rec(int(sec*sr), samplerate=sr, channels=1, dtype="float32", device=device_idx)
    sd.wait()
    return audio.reshape(-1).astype(np.float32)

def once(sec, device_idx, model):
    audio = record_fixed_seconds(sec, device_idx)
    print("[stt] transcribing...")
    text = transcribe_array(model, audio, lang="ko")
    ts = time.strftime("%H:%M:%S")
    print(f"\n[{ts}] {text or '(빈 결과)'}\n")

def loop(sec, device_idx, model):
    i = 1
    try:
        while True:
            print(f"\n=== Chunk {i} ===")
            once(sec, device_idx, model)
            i += 1
    except KeyboardInterrupt:
        print("\n[info] stopped.")

def main():
    ap = argparse.ArgumentParser(description="USB Mic → Korean STT, fixed-length (no VAD)")
    ap.add_argument("--list-devices", action="store_true", help="오디오 장치 목록 출력 후 종료")
    ap.add_argument("--device", type=str, default=None, help="입력 장치 인덱스 또는 이름 일부 (예: 'USB' 또는 '2')")
    ap.add_argument("--sec", type=float, default=10.0, help="녹음 길이(초). 기본 10초")
    ap.add_argument("--model", type=str, default="small", help="faster-whisper 모델 크기 (tiny/base/small/medium/large-v3 등)")
    ap.add_argument("--compute", type=str, default="int8", help="연산 타입 (CPU는 int8 권장)")
    ap.add_argument("--loop", action="store_true", help="고정 길이 녹음을 반복 수행")
    args = ap.parse_args()

    if args.list_devices:
        list_devices()
        return
    
    device_idx = pick_device(args.device) if args.device else None
    model = load_model(args.model, args.compute)


    if args.loop:
        loop(args.sec, device_idx, model)
    else:
        once(args.sec, device_idx, model)

if __name__ == "__main__":
    main()
