import ffmpeg
import numpy as np

def load_audio(file: (str, bytes), sr: int = 16000):
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    file: (str, bytes)
        The audio file to open or bytes of audio file

    sr: int
        The sample rate to resample the audio if necessary

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """

    if isinstance(file, bytes):
        inp = file
        file = 'pipe:'
    else:
        inp = None

    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=inp)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def searcher(trans_dict, query):

    results = []
    segments = trans_dict['segments']

    for segment in segments:
        if query.lower() in segment['text'].lower():

            start_m, start_s = divmod(int(segment['start']), 60)
            end_m, end_s = divmod(int(segment['end']), 60)

            print(f'{start_m:02d}:{start_s:02d} - {end_m:02d}:{end_s:02d}')
            results.append(f'{start_m:02d}:{start_s:02d} - {end_m:02d}:{end_s:02d}')

    return results