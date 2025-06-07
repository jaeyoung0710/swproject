import os
import datetime
import sounddevice as sd
from scipy.io.wavfile import write

RECORD_DURATION = 5  # 초 단위 녹음 시간
SAMPLE_RATE = 44100  # 표준 오디오 샘플링 레이트

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RECORDS_DIR = os.path.join(BASE_PATH, 'records')


def create_records_folder():
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)


def get_filename_by_timestamp():
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M%S')
    return os.path.join(RECORDS_DIR, f'{timestamp}.wav')


def record_audio(filename, duration, sample_rate):
    print('🔴 녹음 시작...')
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(filename, sample_rate, recording)
    print(f'✅ 녹음 완료: {filename}')


def main():
    create_records_folder()
    filename = get_filename_by_timestamp()
    record_audio(filename, RECORD_DURATION, SAMPLE_RATE)


if __name__ == '__main__':
    main()
