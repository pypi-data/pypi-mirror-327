#
# Copyright 2024-2025 Picovoice Inc.
#
# You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
# file accompanying this source.
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

import os
import platform
import subprocess

from ctypes import *
from enum import Enum
from struct import pack
from typing import *

CALLBACK = CFUNCTYPE(None, POINTER(c_int16))

_RASPBERRY_PI_MACHINES = {
    "cortex-a53",
    "cortex-a72",
    "cortex-a76",
    "cortex-a53-aarch64",
    "cortex-a72-aarch64",
    "cortex-a76-aarch64",
}


def _linux_machine() -> str:
    machine = platform.machine()
    if machine == "x86_64":
        return machine
    elif machine in ["aarch64", "armv7l"]:
        arch_info = ("-" + machine) if '64bit' in platform.architecture()[0] else ""
    else:
        raise NotImplementedError("Unsupported CPU architecture: `%s`" % machine)

    cpu_info = ""
    try:
        cpu_info = subprocess.check_output(["cat", "/proc/cpuinfo"]).decode("utf-8")
        cpu_part_list = [x for x in cpu_info.split("\n") if "CPU part" in x]
        cpu_part = cpu_part_list[0].split(" ")[-1].lower()
    except Exception as e:
        raise RuntimeError("Failed to identify the CPU with `%s`\nCPU info: `%s`" % (e, cpu_info))

    if "0xd03" == cpu_part:
        return "cortex-a53" + arch_info
    elif "0xd08" == cpu_part:
        return "cortex-a72" + arch_info
    elif "0xd0b" == cpu_part:
        return "cortex-a76" + arch_info
    else:
        raise NotImplementedError("Unsupported CPU: `%s`." % cpu_part)


def default_library_path(relative: str = ''):
    """A helper function to get the library path."""

    if platform.system() == "Darwin":
        if platform.machine() == "x86_64":
            return os.path.join(os.path.dirname(__file__), relative, "lib/mac/x86_64/libpv_speaker.dylib")
        elif platform.machine() == "arm64":
            return os.path.join(os.path.dirname(__file__), relative, "lib/mac/arm64/libpv_speaker.dylib")
    elif platform.system() == "Linux":
        linux_machine = _linux_machine()
        if linux_machine == "x86_64":
            return os.path.join(os.path.dirname(__file__), relative, "lib/linux/x86_64/libpv_speaker.so")
        elif linux_machine in _RASPBERRY_PI_MACHINES:
            return os.path.join(
                os.path.dirname(__file__), relative, "lib/raspberry-pi/%s/libpv_speaker.so" % linux_machine)
    elif platform.system() == "Windows":
        if platform.machine().lower() == "amd64":
            return os.path.join(os.path.dirname(__file__), relative, "lib/windows/amd64/libpv_speaker.dll")
        elif platform.machine().lower() == "arm64":
            return os.path.join(os.path.dirname(__file__), relative, "lib/windows/arm64/libpv_speaker.dll")

    raise NotImplementedError("Unsupported platform.")


class PvSpeaker(object):
    """
    A cross-platform Python SDK for PvSpeaker to play audio. It lists the available output devices.
    Also given the audio device index, sample_rate, frame_length, and bits_per_sample, plays the
    frame of audio to the device speakers.
    """

    class PvSpeakerStatuses(Enum):
        SUCCESS = 0
        OUT_OF_MEMORY = 1
        INVALID_ARGUMENT = 2
        INVALID_STATE = 3
        BACKEND_ERROR = 4
        DEVICE_ALREADY_INITIALIZED = 5
        DEVICE_NOT_INITIALIZED = 6
        IO_ERROR = 7
        RUNTIME_ERROR = 8

    _PVSPEAKER_STATUS_TO_EXCEPTION = {
        PvSpeakerStatuses.OUT_OF_MEMORY: MemoryError,
        PvSpeakerStatuses.INVALID_ARGUMENT: ValueError,
        PvSpeakerStatuses.INVALID_STATE: ValueError,
        PvSpeakerStatuses.BACKEND_ERROR: SystemError,
        PvSpeakerStatuses.DEVICE_ALREADY_INITIALIZED: ValueError,
        PvSpeakerStatuses.DEVICE_NOT_INITIALIZED: ValueError,
        PvSpeakerStatuses.IO_ERROR: IOError,
        PvSpeakerStatuses.RUNTIME_ERROR: RuntimeError
    }

    class CPvSpeaker(Structure):
        pass

    _library = None
    _relative_library_path = ''

    def __init__(
            self,
            sample_rate: int,
            bits_per_sample: int,
            buffer_size_secs: int = 20,
            device_index: int = -1):
        """
        Constructor

        :param sample_rate: The sample rate of the audio to be played.
        :param bits_per_sample: The number of bits per sample.
        :param buffer_size_secs: The size in seconds of the internal buffer used to buffer pcm data
        - i.e. internal circular buffer will be of size `sample_rate` * `buffer_size_secs`.
        :param device_index: The index of the audio device to use. A value of (-1) will resort to default device.
        """

        library = self._get_library()

        init_func = library.pv_speaker_init
        init_func.argtypes = [
            c_int32,
            c_int32,
            c_int32,
            c_int32,
            POINTER(POINTER(self.CPvSpeaker))
        ]
        init_func.restype = self.PvSpeakerStatuses

        self._handle = POINTER(self.CPvSpeaker)()
        self._sample_rate = sample_rate
        self._bits_per_sample = bits_per_sample
        self._buffer_size_secs = buffer_size_secs

        status = init_func(
            sample_rate, bits_per_sample, buffer_size_secs, device_index, byref(self._handle))
        if status is not self.PvSpeakerStatuses.SUCCESS:
            raise self._PVSPEAKER_STATUS_TO_EXCEPTION[status]("Failed to initialize PvSpeaker.")

        self._delete_func = library.pv_speaker_delete
        self._delete_func.argtypes = [POINTER(self.CPvSpeaker)]
        self._delete_func.restype = None

        self._start_func = library.pv_speaker_start
        self._start_func.argtypes = [POINTER(self.CPvSpeaker)]
        self._start_func.restype = self.PvSpeakerStatuses

        self._stop_func = library.pv_speaker_stop
        self._stop_func.argtypes = [POINTER(self.CPvSpeaker)]
        self._stop_func.restype = self.PvSpeakerStatuses

        self._write_func = library.pv_speaker_write
        self._write_func.argtypes = [POINTER(self.CPvSpeaker), c_char_p, c_int32, POINTER(c_int32)]
        self._write_func.restype = self.PvSpeakerStatuses

        self._flush_func = library.pv_speaker_flush
        self._flush_func.argtypes = [POINTER(self.CPvSpeaker), c_char_p, c_int32, POINTER(c_int32)]
        self._flush_func.restype = self.PvSpeakerStatuses

        self._get_is_started_func = library.pv_speaker_get_is_started
        self._get_is_started_func.argtypes = [POINTER(self.CPvSpeaker)]
        self._get_is_started_func.restype = c_bool

        self._get_selected_device_func = library.pv_speaker_get_selected_device
        self._get_selected_device_func.argtypes = [POINTER(self.CPvSpeaker)]
        self._get_selected_device_func.restype = c_char_p

        self._version_func = library.pv_speaker_version
        self._version_func.argtypes = None
        self._version_func.restype = c_char_p

        self._write_to_file_func = library.pv_speaker_write_to_file
        self._write_to_file_func.argtypes = [POINTER(self.CPvSpeaker), c_char_p]
        self._write_to_file_func.restype = self.PvSpeakerStatuses

    def delete(self) -> None:
        """Releases any resources used by PvSpeaker."""

        self._delete_func(self._handle)

    def start(self) -> None:
        """Starts the audio output device."""

        status = self._start_func(self._handle)
        if status is not self.PvSpeakerStatuses.SUCCESS:
            raise self._PVSPEAKER_STATUS_TO_EXCEPTION[status]("Failed to start device.")

    def stop(self) -> None:
        """Stops the audio output device."""

        status = self._stop_func(self._handle)
        if status is not self.PvSpeakerStatuses.SUCCESS:
            raise self._PVSPEAKER_STATUS_TO_EXCEPTION[status]("Failed to stop device.")

    def _pcm_to_bytes(self, pcm) -> bytes:
        byte_data = None
        if self._bits_per_sample == 8:
            byte_data = pack('B' * len(pcm), *pcm)
        elif self._bits_per_sample == 16:
            byte_data = pack('h' * len(pcm), *pcm)
        elif self._bits_per_sample == 24:
            byte_data = b''.join(pack('<i', sample)[0:3] for sample in pcm)
        elif self._bits_per_sample == 32:
            byte_data = pack('i' * len(pcm), *pcm)
        return byte_data

    def write(self, pcm) -> int:
        """
        Synchronous call to write PCM data to the internal circular buffer for audio playback.
        Only writes as much PCM data as the internal circular buffer can currently fit, and
        returns the length of the PCM data that was successfully written.

        :return: Length of the PCM data that was successfully written.
        """

        written_length = c_int32()
        status = self._write_func(
            self._handle, c_char_p(self._pcm_to_bytes(pcm)), c_int32(len(pcm)), byref(written_length))
        if status is not self.PvSpeakerStatuses.SUCCESS:
            raise self._PVSPEAKER_STATUS_TO_EXCEPTION[status]("Failed to write to device.")

        return written_length.value

    def flush(self, pcm=None) -> int:
        """
        Synchronous call to write PCM data to the internal circular buffer for audio playback.
        This call blocks the thread until all PCM data has been successfully written and played.

        :return: Length of the PCM data that was successfully written.
        """

        if pcm is None:
            pcm = []
        written_length = c_int32()
        status = self._flush_func(
            self._handle, c_char_p(self._pcm_to_bytes(pcm)), c_int32(len(pcm)), byref(written_length))
        if status is not self.PvSpeakerStatuses.SUCCESS:
            raise self._PVSPEAKER_STATUS_TO_EXCEPTION[status]("Failed to flush PCM data.")

        return written_length.value

    def write_to_file(self, output_path: str) -> None:
        """Writes PCM data passed to PvSpeaker to a specified WAV file."""

        status = self._write_to_file_func(self._handle, output_path.encode("utf-8"))
        if status is not self.PvSpeakerStatuses.SUCCESS:
            raise self._PVSPEAKER_STATUS_TO_EXCEPTION[status](
                "Failed to open FILE object. PCM data will not be written.")

    @property
    def is_started(self) -> bool:
        """Gets whether the speaker has started and is available to receive pcm frames or not."""

        return bool(self._get_is_started_func(self._handle))

    @property
    def selected_device(self) -> str:
        """Gets the audio device that the given `PvSpeaker` instance is using."""

        device_name = self._get_selected_device_func(self._handle)
        return device_name.decode('utf-8')

    @property
    def version(self) -> str:
        """Gets the current version of PvSpeaker library."""

        version = self._version_func()
        return version.decode('utf-8')

    @property
    def sample_rate(self) -> int:
        """Gets the sample rate matching the value given to `__init__()`."""

        return self._sample_rate

    @property
    def bits_per_sample(self) -> int:
        """Gets the bits per sample matching the value given to `__init__()`."""

        return self._bits_per_sample

    @property
    def buffer_size_secs(self) -> int:
        """Gets the buffer size in seconds matching the value given to `__init__()`."""

        return self._buffer_size_secs

    @staticmethod
    def get_available_devices() -> List[str]:
        """Gets the list of available audio devices that can be used for playing.

        :return: A list of strings, indicating the names of audio devices.
        """

        get_available_devices_func = PvSpeaker._get_library().pv_speaker_get_available_devices
        get_available_devices_func.argstype = [POINTER(c_int32), POINTER(POINTER(c_char_p))]
        get_available_devices_func.restype = PvSpeaker.PvSpeakerStatuses

        free_available_devices_func = PvSpeaker._get_library().pv_speaker_free_available_devices
        free_available_devices_func.argstype = [c_int32, POINTER(c_char_p)]
        free_available_devices_func.restype = None

        count = c_int32()
        devices = POINTER(c_char_p)()

        status = get_available_devices_func(byref(count), byref(devices))
        if status is not PvSpeaker.PvSpeakerStatuses.SUCCESS:
            raise PvSpeaker._PVSPEAKER_STATUS_TO_EXCEPTION[status]("Failed to get device list")

        device_list = list()
        for i in range(count.value):
            device_list.append(devices[i].decode('utf-8'))

        free_available_devices_func(count, devices)

        return device_list

    @classmethod
    def set_default_library_path(cls, relative: str):
        cls._relative_library_path = default_library_path(relative)

    @classmethod
    def _get_library(cls):
        if len(cls._relative_library_path) == 0:
            cls._relative_library_path = default_library_path()
        if cls._library is None:
            cls._library = cdll.LoadLibrary(cls._relative_library_path)
        return cls._library


__all__ = [
    'PvSpeaker',
]
