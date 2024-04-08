import argparse

# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--output_dir",
    help="Where to save the audio that resulted in an activation",
    type=str,
    default="./",
    required=False,
)
parser.add_argument(
    "--threshold",
    help="The score threshold for an activation",
    type=float,
    default=0.5,
    required=False,
)
parser.add_argument(
    "--vad_threshold",
    help="""The threshold to use for voice activity detection (VAD) in the openWakeWord instance.
            The default (0.0), disables VAD.""",
    type=float,
    default=0.0,
    required=False,
)
parser.add_argument(
    "--noise_suppression",
    help="Whether to enable speex noise suppression in the openWakeWord instance.",
    type=bool,
    default=False,
    required=False,
)
# parser=argparse.ArgumentParser()
parser.add_argument(
    "--chunk_size",
    help="How much audio (in number of 16khz samples) to predict on at once",
    type=int,
    default=1280,
    required=False,
)
parser.add_argument(
    "--model_path",
    help="The path of a specific model to load",
    type=str,
    default="./Wakewords/Echo.onnx",
    required=False,
)
parser.add_argument(
    "--inference_framework",
    help="The inference framework to use (either 'onnx' or 'tflite'",
    type=str,
    default="onnx",
    required=False,
)
parser.add_argument(
    "--disable_activation_sound",
    help="Disables the activation sound, clips are silently captured",
    action="store_true",
    required=False,
)


def gibbe_args():
    return parser.parse_args()
