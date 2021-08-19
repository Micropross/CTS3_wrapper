from enum import IntEnum, unique
from ctypes import c_uint8, c_uint16, c_int32, c_uint32
from ctypes import Structure, byref
from typing import Union, Tuple, List, Optional, overload
from . import _MPuLib, _MPuLib_variadic, _check_limits
from .Measurement import VoltmeterRange
from .Nfc import TechnologyType, NfcTrigger, DataRate
from .Nfc import VicinityDataRate, VicinitySubCarrier
from .MPStatus import CTS3ErrorCode
from .MPException import CTS3Exception


def MPC_OpenScenarioPcd() -> int:
    """Opens a scenario instance

    Returns
    -------
    int
        Scenario instance identifier
    """
    scenario_id = c_uint32()
    ret = CTS3ErrorCode(_MPuLib.MPC_OpenScenarioPcd(
        c_uint8(0),
        byref(scenario_id),
        c_uint32(0)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return scenario_id.value


@unique
class CardEmuSeqAction(IntEnum):
    """Card emulation sequencer actions"""
    TSCN_PARAM_SOF_LOW = 2
    TSCN_PARAM_SOF_HIGH = 3
    TSCN_PARAM_EGT = 4
    TSCN_PARAM_EOF = 5
    TSCN_DO_TEMPO = 19
    TSCN_DO_EXCHANGE = 22
    TSCN_DO_PARITY_ERROR = 23
    TSCN_DO_CHANGE_DATA_RATE = 24
    TSCN_DO_USER_EVENT = 25
    TSCN_DO_TRIGGER_OUT = 26
    TSCN_PARAM_TR0 = 27
    TSCN_PARAM_TR1 = 28
    TSCN_PARAM_TRF = 29
    TSCN_PARAM_FDT1_PICC = 30
    TSCN_PARAM_FDT2_PICC = 31
    TSCN_DO_SEQUENCE_ERROR = 32
    TSCN_DO_EMD = 33
    TSCN_DO_CHANGE_VC_DATA_RATE = 34
    TSCN_DO_COMPLETE_ANTICOLLISION = 35
    TSCN_DO_WAIT_VC_EOF_ONLY = 36
    TSCN_EMD_SUBCARRIER = 37
    TSCN_SET_PCD_MASK = 38
    TSCN_DO_EXCHANGE_RAW_TYPEA = 39
    TSCN_DO_TRIGGER_OUT_RX_ON = 41
    TSCN_DO_TRIGGER_OUT_EMD_GENERATION = 42
    TSCN_DO_WAIT_TYPEA106_SEND_BITS = 43
    TSCN_PARAM_TR0_NS = 50
    TSCN_PARAM_FDT1_PICC_NS = 51
    TSCN_PARAM_FDT2_PICC_NS = 52
    TSCN_PARAM_EGT_BEFORE_EOF = 53
    TSCN_PARAM_FELICA_BIT_CODING_REVERSE = 57
    TSCN_DO_CHANGE_FELICA_DUTY_CYCLE = 58
    TSCN_DO_WAIT_VC_SEND_SOF_ONLY = 63
    TSCN_DO_CE_TRIGGER = 65
    TSCN_DO_START_RF_MEASURE = 67
    TSCN_DO_SELECT_VOLTMETER_RANGE = 69
    TSCN_DO_EXCHANGE_EBF = 70
    TSCN_DO_NEGATIVE_MODULATION = 71
    TSCN_SET_LMA_CARD_EMULATION = 72
    TSCN_DO_VICINITY_COLLISION = 75
    TSCN_PARAM_AUTOMATIC_ATN_RESPONSE = 76
    TSCN_DO_EXCHANGE_ACTIVE_TARGET = 77
    TSCN_PARAM_NFC_ACTIVE_TIMINGS = 78
    TSCN_PARAM_ACTIVE_FDT_MODE = 80


@unique
class SequenceError(IntEnum):
    """Type A sequence error"""
    SEQUENCE_ERROR_C = 1
    SEQUENCE_ERROR_D = 2
    SEQUENCE_ERROR_E = 7


@unique
class EmdSubCarrier(IntEnum):
    """EMD sub-carriers"""
    EMD_64_PERIODS = 212
    EMD_424_PERIODS = 424
    EMD_848_PERIODS = 848
    EMD_1695_PERIODS = 1695
    EMD_3390_PERIODS = 3390
    EMD_6780_PERIODS = 6780


class _S_EMD(Structure):
    """EMD structure definition"""
    _pack_ = 1
    _fields_ = [('nb_pattern', c_uint16),
                ('pattern', c_uint16)]


@unique
class S_EMD_pattern(IntEnum):
    """EMD pattern"""
    high_state = 0
    rising_edge = 1
    falling_edge = 2
    low_state = 3


class S_EMD():
    """EMD definition"""
    def __init__(self, patterns_number: int, pattern_type: S_EMD_pattern):
        """Inits S_EMD class

        Attributes
        ----------
        pattern_number : int
            Patterns number to send
        pattern_type : S_EMD_pattern
            EMD waveform pattern
        """
        _check_limits(c_uint16, patterns_number, 'patterns_number')
        if not isinstance(pattern_type, S_EMD_pattern):
            raise TypeError('pattern_type must be an instance of '
                            'S_EMD_pattern IntEnum')
        self.number = patterns_number
        self.type = pattern_type


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[Union[int, bool, float,
                                      EmdSubCarrier, VoltmeterRange]]) -> None:
    # TSCN_PARAM_SOF_LOW, TSCN_PARAM_SOF_HIGH, TSCN_PARAM_EGT, TSCN_PARAM_EOF,
    # TSCN_DO_PARITY_ERROR, TSCN_DO_USER_EVENT, TSCN_PARAM_TR0, TSCN_PARAM_TR1,
    # TSCN_PARAM_TRF, TSCN_PARAM_FDT1_PICC, TSCN_PARAM_FDT2_PICC,
    # TSCN_PARAM_EGT_BEFORE_EOF, TSCN_DO_COMPLETE_ANTICOLLISION,
    # TSCN_DO_TRIGGER_OUT_RX_ON, TSCN_DO_TRIGGER_OUT_EMD_GENERATION,
    # TSCN_PARAM_AUTOMATIC_ATN_RESPONSE,
    # TSCN_PARAM_FELICA_BIT_CODING_REVERSE, TSCN_PARAM_ACTIVE_FDT_MODE,
    # TSCN_DO_WAIT_VC_EOF_ONLY,
    # TSCN_DO_TEMPO, TSCN_PARAM_TR0_NS, TSCN_PARAM_FDT1_PICC_NS,
    # TSCN_PARAM_FDT2_PICC_NS,
    # TSCN_EMD_SUBCARRIER,
    # TSCN_DO_SELECT_VOLTMETER_RANGE
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[Union[int, bool, VicinityDataRate,
                                            DataRate],
                                      Union[int, bool, VicinitySubCarrier,
                                            DataRate]]) -> None:
    # TSCN_DO_CHANGE_FELICA_DUTY_CYCLE, TSCN_DO_VICINITY_COLLISION,
    # TSCN_DO_TRIGGER_OUT,
    # TSCN_DO_CHANGE_VC_DATA_RATE,
    # TSCN_DO_CHANGE_DATA_RATE,
    # TSCN_DO_NEGATIVE_MODULATION
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, int, int]) -> None:
    # TSCN_DO_NEGATIVE_MODULATION
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[int,
                                      Union[int, NfcTrigger],
                                      Union[int, bool,
                                            SequenceError]]) -> None:
    # TSCN_PARAM_NFC_ACTIVE_TIMINGS,
    # TSCN_DO_CE_TRIGGER,
    # TSCN_DO_SEQUENCE_ERROR
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[Union[float, NfcTrigger],
                                      float]) -> None:
    # TSCN_SET_LMA_CARD_EMULATION,
    # TSCN_DO_START_RF_MEASURE
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[int, List[S_EMD]]) -> None:
    # TSCN_DO_EMD
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, TechnologyType, bool,
                                      bytes]) -> None:
    # TSCN_DO_EXCHANGE
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bool,
                                      TechnologyType, bool,
                                      Optional[bytes],
                                      Optional[bytes]]) -> None:
    # TSCN_DO_EXCHANGE
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bool,
                                      TechnologyType, bool,
                                      bytes, Optional[bytes]]) -> None:
    # TSCN_DO_EXCHANGE_ACTIVE_TARGET
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bytes]) -> None:
    # TSCN_DO_WAIT_VC_EOF_ONLY
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[TechnologyType, bytes]) -> None:
    # TSCN_SET_PCD_MASK
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bytes, bytes]) -> None:
    # TSCN_DO_EXCHANGE_RAW_TYPEA
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bool, bytes]) -> None:
    # TSCN_DO_WAIT_VC_SEND_SOF_ONLY
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, int, bytes]) -> None:
    # TSCN_DO_WAIT_TYPEA106_SEND_BITS
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bool, Optional[bytes]]) -> None:
    # TSCN_DO_WAIT_TYPEA106_SEND_BITS
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bool, Optional[bytes],
                                      int, bytes]) -> None:
    # TSCN_DO_WAIT_TYPEA106_SEND_BITS
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bool, int, int, bool,
                                      TechnologyType, bool, bytes]) -> None:
    # TSCN_DO_EXCHANGE_EBF
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         *args: Tuple[bool, bool, int, int, bool, bool,
                                      TechnologyType, bool,
                                      bytes, Optional[bytes]]) -> None:
    # TSCN_DO_EXCHANGE_EBF
    ...


def MPC_AddToScenarioPcd(scenario_id: int,
                         action: CardEmuSeqAction,
                         *args: Union[Tuple[Union[int, bool, float,
                                                  EmdSubCarrier,
                                                  VoltmeterRange]],
                                      Tuple[Union[int, bool, VicinityDataRate,
                                                  DataRate],
                                            Union[int, bool,
                                                  VicinitySubCarrier,
                                                  DataRate]],
                                      Tuple[bool, int, int],
                                      Tuple[int,
                                            Union[int, NfcTrigger],
                                            Union[int, bool,
                                                  SequenceError]],
                                      Tuple[Union[float, NfcTrigger], float],
                                      Tuple[NfcTrigger, float],
                                      Tuple[int, List[S_EMD]],
                                      Tuple[bool, TechnologyType, bool,
                                            bytes],
                                      Tuple[bool, bool,
                                            TechnologyType, bool,
                                            Optional[bytes],
                                            Optional[bytes]],
                                      Tuple[bool, int, bytes],
                                      Tuple[bool, Optional[bytes]],
                                      Tuple[TechnologyType, bytes],
                                      Tuple[bool, bytes, bytes],
                                      Tuple[bool, bool, Optional[bytes]],
                                      Tuple[bool, bool, Optional[bytes],
                                            int, bytes],
                                      Tuple[bool, bool, bytes],
                                      Tuple[bool, bool, int, int, bool,
                                            TechnologyType, bool, bytes],
                                      Tuple[bool, bool, int, int, bool, bool,
                                            TechnologyType, bool,
                                            bytes, Optional[bytes]]]) -> None:
    """Adds an action to a scenario

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    action : TerminalEmulationSequenceAction
        Scenario action
    args
        Scenario action parameters
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    if not isinstance(action, CardEmuSeqAction):
        raise TypeError('action must be an instance of '
                        'CardEmuSeqAction IntEnum')
    if _MPuLib_variadic is None:
        func_pointer = _MPuLib.MPC_AddToScenarioPcd
    else:
        func_pointer = _MPuLib_variadic.MPC_AddToScenarioPcd

    # One parameter
    if action == CardEmuSeqAction.TSCN_PARAM_SOF_LOW or \
            action == CardEmuSeqAction.TSCN_PARAM_SOF_HIGH or \
            action == CardEmuSeqAction.TSCN_PARAM_EGT or \
            action == CardEmuSeqAction.TSCN_PARAM_EOF or \
            action == CardEmuSeqAction.TSCN_DO_PARITY_ERROR or \
            action == CardEmuSeqAction.TSCN_PARAM_TR0 or \
            action == CardEmuSeqAction.TSCN_PARAM_TR1 or \
            action == CardEmuSeqAction.TSCN_PARAM_TRF or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT1_PICC or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT2_PICC or \
            action == CardEmuSeqAction.TSCN_PARAM_EGT_BEFORE_EOF or \
            action == CardEmuSeqAction.TSCN_PARAM_AUTOMATIC_ATN_RESPONSE or \
            action == CardEmuSeqAction.TSCN_DO_USER_EVENT:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))
    elif action == CardEmuSeqAction.TSCN_PARAM_FELICA_BIT_CODING_REVERSE or \
            action == CardEmuSeqAction.TSCN_PARAM_ACTIVE_FDT_MODE:
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(1) if args[0] else c_uint32(0)))
    # µs
    elif action == CardEmuSeqAction.TSCN_DO_TEMPO:
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of float')
        tempo_us = round(args[0] * 1e6)
        _check_limits(c_uint32, tempo_us, 'args[0]')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(tempo_us)))
    # ns
    elif action == CardEmuSeqAction.TSCN_PARAM_TR0_NS or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT1_PICC_NS or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT2_PICC_NS:
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of float')
        delay_ns = round(args[0] * 1e9)
        _check_limits(c_uint32, delay_ns, 'args[0]')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(delay_ns)))
    elif action == CardEmuSeqAction.TSCN_EMD_SUBCARRIER:
        if not isinstance(args[0], EmdSubCarrier):
            raise TypeError('args[0] must be an instance of '
                            'EmdSubCarrier IntEnum')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            args[0]))
    elif action == CardEmuSeqAction.TSCN_DO_SELECT_VOLTMETER_RANGE:
        if not isinstance(args[0], VoltmeterRange):
            raise TypeError('args[0] must be an instance of '
                            'VoltmeterRange IntEnum')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))

    # Two parameters
    elif action == CardEmuSeqAction.TSCN_DO_CHANGE_FELICA_DUTY_CYCLE or \
            action == CardEmuSeqAction.TSCN_DO_VICINITY_COLLISION:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')
        if not isinstance(args[1], int):
            raise TypeError('args[1] must be an instance of int')
        _check_limits(c_uint32, args[1], 'args[1]')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),
            c_uint32(args[1])))
    elif action == CardEmuSeqAction.TSCN_DO_TRIGGER_OUT:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')  # Trigger
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(1) if args[1] else c_uint32(0)))  # State
    elif action == CardEmuSeqAction.TSCN_DO_CHANGE_VC_DATA_RATE:
        if not isinstance(args[0], VicinityDataRate):
            raise TypeError('args[0] must be an instance of '
                            'VicinityDataRate IntEnum')
        if not isinstance(args[1], VicinitySubCarrier):
            raise TypeError('args[1] must be an instance of '
                            'VicinitySubCarrier IntEnum')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # DataRate
            c_uint32(args[1])))  # SubCarrierNumber
    elif action == CardEmuSeqAction.TSCN_DO_CHANGE_DATA_RATE:
        if not isinstance(args[0], DataRate):
            raise TypeError('args[0] must be an instance of DataRate IntEnum')
        if not isinstance(args[1], DataRate):
            raise TypeError('args[1] must be an instance of DataRate IntEnum')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # PcdDataRate
            c_uint32(args[1])))  # PiccDataRate
    elif action == CardEmuSeqAction.TSCN_DO_TRIGGER_OUT_RX_ON or \
            action == CardEmuSeqAction.TSCN_DO_TRIGGER_OUT_EMD_GENERATION:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')  # Trigger
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(0)))  # Rfu
    elif action == CardEmuSeqAction.TSCN_DO_START_RF_MEASURE:
        if not isinstance(args[0], NfcTrigger):
            raise TypeError('args[0] must be an instance of '
                            'NfcTrigger IntEnum')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('args[1] must be an instance of float')
        delay_ns = round(args[1] * 1e9)
        _check_limits(c_int32, delay_ns, 'args[1]')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # EventMode
            c_int32(delay_ns)))  # Delay_ns
    elif action == CardEmuSeqAction.TSCN_DO_COMPLETE_ANTICOLLISION:
        if not isinstance(args[1], int):
            raise TypeError('args[1] must be an instance of int')
        _check_limits(c_uint32, args[1], 'args[1]')  # Sak
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(1) if args[0] else c_uint32(0),  # Option
            c_uint32(args[1])))  # Sak
    elif action == CardEmuSeqAction.TSCN_SET_LMA_CARD_EMULATION:
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of float')
        low_mV = round(args[0] * 1e3)
        _check_limits(c_int32, low_mV, 'args[0]')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('args[1] must be an instance of float')
        high_mV = round(args[1] * 1e3)
        _check_limits(c_int32, high_mV, 'args[1]')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_int32(low_mV),  # Low_mV
            c_int32(high_mV)))  # High_mV

    # Three parameters
    elif action == CardEmuSeqAction.TSCN_DO_CE_TRIGGER:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')  # Trigger
        if not isinstance(args[1], NfcTrigger):
            raise TypeError('args[1] must be an instance of '
                            'NfcTrigger IntEnum')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(args[1]),  # Config
            c_uint32(1) if args[2] else c_uint32(0)))  # Value
    elif action == CardEmuSeqAction.TSCN_DO_SEQUENCE_ERROR:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')  # ByteNumber
        if not isinstance(args[1], int):
            raise TypeError('args[1] must be an instance of int')
        _check_limits(c_uint32, args[1], 'args[1]')  # SequenceNumber
        if not isinstance(args[2], SequenceError):
            raise TypeError('args[2] must be an instance of '
                            'SequenceError IntEnum')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # ByteNumber
            c_uint32(args[1]),  # SequenceNumber
            c_uint32(args[2])))  # Sequence
    elif action == CardEmuSeqAction.TSCN_PARAM_NFC_ACTIVE_TIMINGS:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')  # NtrfwTadt
        if not isinstance(args[1], int):
            raise TypeError('args[1] must be an instance of int')
        _check_limits(c_uint32, args[1], 'args[1]')  # Tarfg
        if not isinstance(args[2], int):
            raise TypeError('args[2] must be an instance of int')
        _check_limits(c_uint32, args[2], 'args[2]')  # FieldDelay
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # NtrfwTadt
            c_uint32(args[1]),  # Tarfg
            c_uint32(args[2])))  # FieldDelay

    # Two or three parameters
    elif action == CardEmuSeqAction.TSCN_DO_NEGATIVE_MODULATION:
        if not isinstance(args[1], int):
            raise TypeError('args[1] must be an instance of int')
        _check_limits(c_uint32, args[1], 'args[1]')  # TimeBeforeTload_clk
        if len(args) > 2:
            if not isinstance(args[2], int):
                raise TypeError('args[2] must be an instance of int')
            _check_limits(c_uint32, args[2], 'args[2]')  # TimeBeforeTload_clk2
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(0x80000000 + action),
                c_uint32(1) if args[0] else c_uint32(0),  # OnOff
                c_uint32(args[1]),  # TimeBeforeTload_clk
                c_uint32(args[2])))  # TimeBeforeTload_clk2
        else:
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(1) if args[0] else c_uint32(0),  # OnOff
                c_uint32(args[1])))  # TimeBeforeTload_clk

    # Structure parameter
    elif action == CardEmuSeqAction.TSCN_DO_EMD:
        if not isinstance(args[0], int):
            raise TypeError('args[0] must be an instance of int')
        _check_limits(c_uint32, args[0], 'args[0]')  # FdtEmd
        if not isinstance(args[1], list):
            raise TypeError('args[1] must be an instance of S_EMD list')
        emd = (_S_EMD * (len(args[1]) + 1))()
        for i in range(len(args[1])):
            if not isinstance(args[1][i], S_EMD):
                raise TypeError('args[1] must be an instance of '
                                'S_EMD list')
            emd[i] = _S_EMD(c_uint16(args[1][i].number),
                            c_uint16(args[1][i].type.value))
        emd[len(args[1])] = _S_EMD(c_uint16(0), c_uint16(0))
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # FdtEmd
            c_uint32(0),  # Rfu
            emd))  # pPattern

    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE:
        if len(args) > 5:
            if not isinstance(args[2], TechnologyType):
                raise TypeError('args[2] must be an instance of '
                                'TechnologyType IntEnum')
            if args[4] is None:
                pcd_length = 1000000  # PCD_FRAME_DONT_CARE
                pcd_data = bytes()
            else:
                if not isinstance(args[4], bytes):
                    raise TypeError('args[4] must be an instance of bytes')
                _check_limits(c_uint32, len(args[4]), 'args[4]')
                pcd_length = len(args[4])
                pcd_data = args[4]
            if args[5] is not None:
                picc_length = 0
                picc_data = bytes()
            else:
                if not isinstance(args[5], bytes):
                    raise TypeError('args[5] must be an instance of bytes')
                _check_limits(c_uint32, len(args[5]), 'args[5]')
                picc_length = len(args[5])
                picc_data = args[5]
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(2) if args[1] else c_uint32(1),  # PiccCrc
                c_uint32(args[1]),  # PcdFrameType
                c_uint32(1) if args[2] else c_uint32(0),  # Synchro
                c_uint32(pcd_length),  # PcdFrameLength
                pcd_data,  # pExpectedPcdFrame
                c_uint32(picc_length),  # PiccFrameLength
                picc_data,  # pPiccResponse
                ''.encode('ascii')))
        else:
            if not isinstance(args[1], TechnologyType):
                raise TypeError('args[1] must be an instance of '
                                'TechnologyType IntEnum')
            if not isinstance(args[3], bytes):
                raise TypeError('args[3] must be an instance of bytes')
            _check_limits(c_uint32, len(args[3]), 'args[3]')
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(1),  # PcdCrc
                c_uint32(2) if args[0] else c_uint32(1),  # PiccCrc
                c_uint32(args[1]),  # PcdFrameType
                c_uint32(1) if args[2] else c_uint32(0),  # Synchro
                c_uint32(0),  # PcdFrameLength
                bytes(),  # pExpectedPcdFrame
                c_uint32(len(args[3])),  # PiccFrameLength
                args[3],  # pPiccResponse
                ''.encode('ascii')))

    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE_ACTIVE_TARGET:
        if not isinstance(args[2], TechnologyType):
            raise TypeError('args[2] must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[4], bytes):
            raise TypeError('args[4] must be an instance of bytes')
        _check_limits(c_uint32, len(args[4]), 'args[4]')
        if args[5] is None:
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(2) if args[1] else c_uint32(1),  # PiccCrc
                c_uint32(args[2]),  # PcdFrameType
                c_uint32(1) if args[3] else c_uint32(0),  # Synchro
                c_uint32(len(args[4])),  # PcdFrameLength
                args[4],  # pExpectedPcdFrame
                c_uint32(0),  # PiccFrameLength
                bytes()))  # pPiccResponse
        else:
            if args[5] and not isinstance(args[5], bytes):
                raise TypeError('args[5] must be an instance of bytes')
            _check_limits(c_uint32, len(args[5]), 'args[5]')
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(2) if args[1] else c_uint32(1),  # PiccCrc
                c_uint32(args[2]),  # PcdFrameType
                c_uint32(1) if args[3] else c_uint32(0),  # Synchro
                c_uint32(len(args[4])),  # PcdFrameLength
                args[4],  # pExpectedPcdFrame
                c_uint32(len(args[5])),  # PiccFrameLength
                args[5]))  # pPiccResponse

    elif action == CardEmuSeqAction.TSCN_DO_WAIT_VC_EOF_ONLY:
        if len(args) > 1:
            if not isinstance(args[1], bytes):
                raise TypeError('args[1] must be an instance of bytes')
            _check_limits(c_uint32, len(args[1]), 'args[1]')
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PiccCrc
                c_uint32(len(args[1])),  # PiccFrameLength
                args[1],  # pAnswer
                c_uint32(0)))  # pRfu
        else:
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PiccCrc
                c_uint32(0),  # PiccFrameLength
                bytes(),  # pAnswer
                c_uint32(0)))  # pRfu

    elif action == CardEmuSeqAction.TSCN_SET_PCD_MASK:
        if not isinstance(args[0], TechnologyType):
            raise TypeError('args[0] must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[1], bytes):
            raise TypeError('args[1] must be an instance of bytes')
        _check_limits(c_uint32, len(args[1]), 'args[1]')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # PcdFrameType
            c_uint32(len(args[1])),  # MaskLength
            args[1]))  # pPcdMask

    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE_RAW_TYPEA:
        if not isinstance(args[1], bytes):
            raise TypeError('args[1] must be an instance of bytes')
        if not isinstance(args[2], bytes):
            raise TypeError('args[2] must be an instance of bytes')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(TechnologyType.TYPE_A),  # PcdFrameType
            c_uint32(1) if args[0] else c_uint32(0),  # Synchro
            args[1].hex().encode('ascii'),  # pExpectedPcdFrame
            args[2].hex().encode('ascii')))  # pPiccResponse

    elif action == CardEmuSeqAction.TSCN_DO_WAIT_VC_SEND_SOF_ONLY:
        if not isinstance(args[2], bytes):
            raise TypeError('args[2] must be an instance of bytes')
        ret = CTS3ErrorCode(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(1) if args[0] else c_uint32(0),  # VcdCrc
            c_uint32(1) if args[1] else c_uint32(0),  # Synchro
            c_uint32(len(args[2])),  # VcdFrameLength
            args[2]))  # pExpectedVcdFrame

    elif action == CardEmuSeqAction.TSCN_DO_WAIT_TYPEA106_SEND_BITS:
        if len(args) > 4:
            if not isinstance(args[3], int):
                raise TypeError('args[3] must be an instance of int')
            _check_limits(c_uint32, args[3], 'args[3]')  # PiccFrameLength
            if not isinstance(args[4], bytes):
                raise TypeError('args[4] must be an instance of bytes')
            if args[2] is None:
                ret = CTS3ErrorCode(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(1000000),  # PCD_FRAME_DONT_CARE
                    bytes(),  # pExpectedPcdFrame
                    c_uint32(args[3]),  # PiccFrameLength
                    args[4]))  # pPiccResponse
            else:
                if not isinstance(args[2], bytes):
                    raise TypeError('args[2] must be an instance of bytes')
                _check_limits(c_uint32, args[2], 'args[2]')  # PcdFrameLength
                ret = CTS3ErrorCode(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(len(args[2])),  # PcdFrameLength
                    args[2],  # pExpectedPcdFrame
                    c_uint32(args[3]),  # PiccFrameLength
                    args[4]))  # pPiccResponse
        elif isinstance(args[1], int):
            _check_limits(c_uint32, args[1], 'args[1]')  # PiccFrameLength
            if not isinstance(args[2], bytes):
                raise TypeError('args[2] must be an instance of bytes')
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(1),  # PcdCrc
                c_uint32(1) if args[0] else c_uint32(0),  # Synchro
                c_uint32(0),  # PcdFrameLength
                bytes(),  # pExpectedPcdFrame
                c_uint32(args[1]),  # PiccFrameLength
                args[2]))  # pPiccResponse
        else:
            if args[2] is None:
                ret = CTS3ErrorCode(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(1000000),  # PCD_FRAME_DONT_CARE
                    bytes(),  # pExpectedPcdFrame
                    c_uint32(0),  # PiccFrameLength
                    bytes()))  # pPiccResponse
            else:
                if not isinstance(args[2], bytes):
                    raise TypeError('args[2] must be an instance of bytes')
                _check_limits(c_uint32, args[2], 'args[2]')  # PcdFrameLength
                ret = CTS3ErrorCode(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(len(args[2])),  # PcdFrameLength
                    args[2],  # pExpectedPcdFrame
                    c_uint32(0),  # PiccFrameLength
                    bytes()))  # pPiccResponse

    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE_EBF:
        if not isinstance(args[2], int):
            raise TypeError('args[2] must be an instance of int')
        _check_limits(c_uint32, args[2], 'args[2]')  # FrameOptionPcdToPicc
        if not isinstance(args[3], int):
            raise TypeError('args[3] must be an instance of int')
        _check_limits(c_uint32, args[3], 'args[3]')  # FrameOptionPiccToPcd
        if len(args) > 9:
            if not isinstance(args[6], TechnologyType):
                raise TypeError('args[6] must be an instance of '
                                'TechnologyType IntEnum')
            if not isinstance(args[8], bytes):
                raise TypeError('args[8] must be an instance of bytes')
            _check_limits(c_uint32, len(args[8]), 'args[8]')
            if args[9] is None:
                ret = CTS3ErrorCode(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(1) if args[0] else c_uint32(0),  # PcdUseEBF
                    c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                    c_uint32(args[2]),  # FrameOptionPcdToPicc
                    c_uint32(args[3]),  # FrameOptionPiccToPcd
                    c_uint32(2) if args[4] else c_uint32(1),  # PcdCrc
                    c_uint32(2) if args[5] else c_uint32(1),  # PiccCrc
                    c_uint32(args[6]),  # PcdFrameType
                    c_uint32(1) if args[7] else c_uint32(0),  # Synchro
                    c_uint32(len(args[8])),  # PcdFrameLength
                    args[8],  # pExpectedPcdFrame
                    c_uint32(0),  # PiccFrameLength
                    bytes()))  # pPiccResponse
            else:
                if not isinstance(args[9], bytes):
                    raise TypeError('args[9] must be an instance of bytes')
                _check_limits(c_uint32, len(args[9]), 'args[9]')
                ret = CTS3ErrorCode(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(1) if args[0] else c_uint32(0),  # PcdUseEBF
                    c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                    c_uint32(args[2]),  # FrameOptionPcdToPicc
                    c_uint32(args[3]),  # FrameOptionPiccToPcd
                    c_uint32(2) if args[4] else c_uint32(1),  # PcdCrc
                    c_uint32(2) if args[5] else c_uint32(1),  # PiccCrc
                    c_uint32(args[6]),  # PcdFrameType
                    c_uint32(1) if args[7] else c_uint32(0),  # Synchro
                    c_uint32(len(args[8])),  # PcdFrameLength
                    args[8],  # pExpectedPcdFrame
                    c_uint32(len(args[9])),  # PiccFrameLength
                    args[9]))  # pPiccResponse
        else:
            if not isinstance(args[5], TechnologyType):
                raise TypeError('args[5] must be an instance of '
                                'TechnologyType IntEnum')
            if not isinstance(args[7], bytes):
                raise TypeError('args[7] must be an instance of bytes')
            _check_limits(c_uint32, len(args[7]), 'args[7]')
            ret = CTS3ErrorCode(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(1) if args[0] else c_uint32(0),  # PcdUseEBF
                c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                c_uint32(args[2]),  # FrameOptionPcdToPicc
                c_uint32(args[3]),  # FrameOptionPiccToPcd
                c_uint32(1),  # PcdCrc
                c_uint32(2) if args[5] else c_uint32(1),  # PiccCrc
                c_uint32(args[6]),  # PcdFrameType
                c_uint32(1) if args[6] else c_uint32(0),  # Synchro
                c_uint32(0),  # PcdFrameLength
                bytes(),  # pExpectedPcdFrame
                c_uint32(len(args[7])),  # PiccFrameLength
                args[7]))  # pPiccResponse

    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_ExecuteScenarioPcd(scenario_id: int, timeout: float) -> None:
    """Runs a scenario instance

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    timeout : float
        Scenario timeout in s
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    ret = CTS3ErrorCode(_MPuLib.MPC_ExecuteScenarioPcd(
        c_uint8(0),
        c_uint32(scenario_id),
        c_uint32(timeout_ms)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_CloseScenarioPcd(scenario_id: int) -> None:
    """Closes a scenario instance

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    ret = CTS3ErrorCode(_MPuLib.MPC_CloseScenarioPcd(
        c_uint8(0),
        c_uint32(scenario_id)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
