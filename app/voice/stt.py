import sounddevice as sd
import numpy as np
import queue
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

class STTAgent:
    _processor = None
    _model = None

    def __init__(self, sampling_rate=16000):
        self.sampling_rate = sampling_rate
        self.q = queue.Queue()
        self.stream = None

        if STTAgent._processor is None or STTAgent._model is None:
            STTAgent._processor = WhisperProcessor.from_pretrained(
                "openai/whisper-small"
            )
            STTAgent._model = WhisperForConditionalGeneration.from_pretrained(
                "openai/whisper-small"
            ).to("cpu")

        self.processor = STTAgent._processor
        self.model = STTAgent._model

    def _callback(self, indata, frames, time, status):
        if status:
            print("Audio status:", status)

        try:
            self.q.put_nowait(indata.copy())
        except queue.Full:
            pass  



    def start_recording(self):
        with self.q.mutex:
            self.q.queue.clear()

        self.stream = sd.InputStream(
            samplerate=self.sampling_rate,
            channels=1,
            dtype="float32",
            callback=self._callback
        )
        self.stream.start()

    def stop_and_transcribe(self):
        self.stream.stop()
        self.stream.close()

        audio_chunks = []
        while not self.q.empty():
            audio_chunks.append(self.q.get())

        if not audio_chunks:
            return ""

        audio = np.concatenate(audio_chunks, axis=0).squeeze()

        inputs = self.processor(
            audio,
            sampling_rate=self.sampling_rate,
            return_tensors="pt"
        )

        with torch.no_grad():
            predicted_ids = self.model.generate(
                inputs.input_features,
                language="en"
            )

        transcription = self.processor.batch_decode(
            predicted_ids,
            skip_special_tokens=True
        )[0]

        return transcription.strip()
