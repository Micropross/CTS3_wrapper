from ctypes import c_uint8, c_uint16, c_uint32, c_int32, byref, Structure
from typing import Optional, Union, Dict
from enum import IntEnum, IntFlag, unique
from . import _MPuLib, _check_limits
from .Nfc import VicinityDataRate, VicinitySubCarrier, NfcMode
from .Nfc import TechnologyType, NfcDataRate
from .MPStatus import CTS3ErrorCode
from .MPException import CTS3Exception


@unique
class IsoSimulatorEvent(IntFlag):
    """ISO 14443 simulation events"""
    SIM_EVT_CL_14443_FRAME_RECEIVED = 1 << 0
    SIM_EVT_CL_14443_FRAME_SENT = 1 << 1
    SIM_EVT_CL_14443_APDU_RECEIVED = 1 << 2
    SIM_EVT_CL_14443_RAPDU_SENT = 1 << 3
    SIM_EVT_CL_14443_PPS_REQUEST = 1 << 4
    SIM_EVT_CL_14443_PPS_RESPONSE_SENT = 1 << 5
    SIM_EVT_CL_14443_WTX_REQUEST_SENT = 1 << 6
    SIM_EVT_CL_14443_WTX_RESPONSE_RECEIVED = 1 << 7
    SIM_EVT_CL_14443_DESELECT_RESPONSE_SENT = 1 << 8
    SIM_EVT_CL_FIELD_POWER_ON = 1 << 9
    SIM_EVT_CL_FIELD_POWER_OFF = 1 << 10
    SIM_EVT_CL_14443_DESELECT_RECEIVED = 1 << 11
    SIM_EVT_CL_14443_RACK_RECEIVED = 1 << 12
    SIM_EVT_CL_14443_RNACK_RECEIVED = 1 << 13
    SIM_EVT_CL_14443_SPARAM_RECEIVED = 1 << 14
    SIM_EVT_CL_14443_REQA_RECEIVED = 1 << 15
    SIM_EVT_CL_14443_WUPA_RECEIVED = 1 << 16
    SIM_EVT_CL_14443_HLTA_RECEIVED = 1 << 17
    SIM_EVT_CL_14443_ANTICOLLA_RECEIVED = 1 << 18
    SIM_EVT_CL_14443_SELECTA_RECEIVED = 1 << 19
    SIM_EVT_CL_14443_RATS_RECEIVED = 1 << 20
    SIM_EVT_CL_14443_RATS_RESPONSE_SENT = 1 << 21
    SIM_EVT_CL_14443_REQB_RECEIVED = 1 << 25
    SIM_EVT_CL_14443_WUPB_RECEIVED = 1 << 26
    SIM_EVT_CL_14443_HLTB_RECEIVED = 1 << 27
    SIM_EVT_CL_14443_ATTRIB_RECEIVED = 1 << 28
    SIM_EVT_CL_14443_ATTRIB_RESPONSE_SENT = 1 << 29
    SIM_EVT_CL_14443_HLTB_RESPONSE_SENT = 1 << 30
    SIM_EVT_CL_14443_SPARAM_SENT = 1 << 31


@unique
class Type2TagSimulatorEvent(IntFlag):
    """NFC Type 2 Tag simulation events"""
    SIM_EVT_CL_14443_FRAME_RECEIVED = 1 << 0
    SIM_EVT_CL_14443_FRAME_SENT = 1 << 1
    SIM_EVT_CL_FIELD_POWER_ON = 1 << 9
    SIM_EVT_CL_FIELD_POWER_OFF = 1 << 10
    SIM_EVT_CL_14443_REQA_RECEIVED = 1 << 15
    SIM_EVT_CL_14443_WUPA_RECEIVED = 1 << 16
    SIM_EVT_CL_14443_HLTA_RECEIVED = 1 << 17
    SIM_EVT_CL_14443_ANTICOLLA_RECEIVED = 1 << 18
    SIM_EVT_CL_14443_SELECTA_RECEIVED = 1 << 19


@unique
class FeliCaSimulatorEvent(IntFlag):
    """FeliCa simulation events"""
    SIM_EVT_CL_FELICA_FRAME_RECEIVED = 1 << 0
    SIM_EVT_CL_FELICA_FRAME_SENT = 1 << 1
    SIM_EVT_CL_FIELD_POWER_ON = 1 << 9
    SIM_EVT_CL_FIELD_POWER_OFF = 1 << 10


@unique
class VicinitySimulatorEvent(IntFlag):
    """Vicinity simulation events"""
    SIM_EVT_CL_VICINITY_FRAME_RECEIVED = 1 << 0
    SIM_EVT_CL_VICINITY_FRAME_SENT = 1 << 1
    SIM_EVT_CL_FIELD_POWER_ON = 1 << 9
    SIM_EVT_CL_FIELD_POWER_OFF = 1 << 10


@unique
class NfcSimulatorEvent(IntFlag):
    """NFC simulation events"""
    SIM_EVT_CL_NFC_FRAME_RECEIVED = 1 << 0
    SIM_EVT_CL_NFC_FRAME_SENT = 1 << 1
    SIM_EVT_CL_NFC_UDATA_RECEIVED = 1 << 2
    SIM_EVT_CL_NFC_UDATA_SENT = 1 << 3
    SIM_EVT_CL_NFC_ATR_REQ_RECEIVED = 1 << 4
    SIM_EVT_CL_NFC_ATR_RES_SENT = 1 << 5
    SIM_EVT_CL_NFC_ERROR = 1 << 6
    SIM_EVT_CL_NFC_ACK_RECEIVED = 1 << 7
    SIM_EVT_CL_NFC_ACK_SENT = 1 << 8
    SIM_EVT_CL_FIELD_POWER_ON = 1 << 9
    SIM_EVT_CL_FIELD_POWER_OFF = 1 << 10
    SIM_EVT_CL_NFC_NACK_RECEIVED = 1 << 11
    SIM_EVT_CL_NFC_NACK_SENT = 1 << 12
    SIM_EVT_CL_NFC_PSL_REQ_RECEIVED = 1 << 13
    SIM_EVT_CL_NFC_PSL_RES_SENT = 1 << 14
    SIM_EVT_CL_NFC_DSL_REQ_RECEIVED = 1 << 15
    SIM_EVT_CL_NFC_DSL_RES_SENT = 1 << 16
    SIM_EVT_CL_NFC_RLS_REQ_RECEIVED = 1 << 17
    SIM_EVT_CL_NFC_RLS_RES_SENT = 1 << 18
    SIM_EVT_CL_NFC_WUP_REQ_RECEIVED = 1 << 19
    SIM_EVT_CL_NFC_WUP_RES_SENT = 1 << 20
    SIM_EVT_CL_NFC_RTOX_SENT = 1 << 21
    SIM_EVT_CL_NFC_RTOX_RES_RECEIVED = 1 << 22
    SIM_EVT_CL_NFC_ATTENTION_RECEIVED = 1 << 23
    SIM_EVT_CL_NFC_TARGET_PRESENT_SENT = 1 << 24
    SIM_EVT_CL_NFC_SENS_REQ_RECEIVED = 1 << 25
    SIM_EVT_CL_NFC_ALL_REQ_RECEIVED = 1 << 26
    SIM_EVT_CL_NFC_SLP_REQ_RECEIVED = 1 << 27
    SIM_EVT_CL_NFC_SDD_REQ_RECEIVED = 1 << 28
    SIM_EVT_CL_NFC_SEL_REQ_RECEIVED = 1 << 29
    SIM_EVT_CL_NFC_POLLING_REQUEST_RECEIVED = 1 << 30
    SIM_EVT_CL_NFC_POLLING_RESPONSE_SENT = 1 << 31

# region Simulation initialization


def MPC_Set14443AInitParameters(atqa: bytes, uid: bytes,
                                sak: Union[bytes, int],
                                ats: Optional[bytes]) -> None:
    """Initializes Type A simulation parameters

    Parameters
    ----------
    atqa : bytes
        2-byte ATQA to answer
    uid : bytes or int
        UID to answer
    sak : bytes or int
        SAK byte to answer
    ats : bytes
        ATS to answer
    """
    if not isinstance(atqa, bytes) or len(atqa) != 2:
        raise TypeError('atqa must be an instance of 2 bytes')
    if not isinstance(uid, bytes):
        raise TypeError('uid must be an instance of bytes')
    _check_limits(c_uint32, len(uid), 'uid')
    if isinstance(sak, bytes):
        if len(sak) != 1:
            raise TypeError('sak must be an instance of 1 byte')
        sak_value = sak[0]
    elif isinstance(sak, int):
        _check_limits(c_uint8, sak, 'sak')
        sak_value = sak
    else:
        raise TypeError('sak must be an instance of int or 1 byte')
    if ats:
        if not isinstance(ats, bytes):
            raise TypeError('ats must be an instance of bytes')
        _check_limits(c_uint32, len(ats), 'ats')
        ret = CTS3ErrorCode(_MPuLib.MPC_Set14443AInitParameters(
            c_uint8(0),
            atqa,
            c_uint32(len(uid)),
            uid,
            byref(c_uint8(sak_value)),
            c_uint32(len(ats)),
            ats))
    else:
        ret = CTS3ErrorCode(_MPuLib.MPC_Set14443AInitParameters(
            c_uint8(0),
            atqa,
            c_uint32(len(uid)),
            uid,
            byref(c_uint8(sak_value)),
            c_uint32(0),
            None))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_WaitTypeAActiveState(atqa: bytes, uid: bytes,
                             sak: Union[bytes, int],
                             timeout: float) -> None:
    """Waits for Type A activation

    Parameters
    ----------
    atqa : bytes
        2-byte ATQA to answer
    uid : bytes or int
        UID to answer
    sak : bytes
        SAK byte to answer
    timeout : float
        Activation timeout in s
    """
    if not isinstance(atqa, bytes) or len(atqa) != 2:
        raise TypeError('atqa must be an instance of 2 bytes')
    if not isinstance(uid, bytes):
        raise TypeError('uid must be an instance of bytes')
    _check_limits(c_uint32, len(uid), 'uid')
    if isinstance(sak, bytes):
        if len(sak) != 1:
            raise TypeError('sak must be an instance of 1 byte')
        sak_value = sak[0]
    elif isinstance(sak, int):
        _check_limits(c_uint8, sak, 'sak')
        sak_value = sak
    else:
        raise TypeError('sak must be an instance of int or 1 byte')
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    ret = CTS3ErrorCode(_MPuLib.MPC_WaitTypeAActiveState(
        c_uint8(0),
        atqa,
        uid,
        c_uint32(len(uid)),
        byref(c_uint8(sak_value)),
        c_uint32(timeout_ms)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_Set14443BInitParameters(atqb: bytes) -> None:
    """Initializes Type B simulation parameters

    Parameters
    ----------
    atqb : bytes
        ATQB to answer
    """
    if not isinstance(atqb, bytes):
        raise TypeError('atqb must be an instance of bytes')
    _check_limits(c_uint32, len(atqb), 'atqb')
    ret = CTS3ErrorCode(_MPuLib.MPC_Set14443BInitParameters(
        c_uint8(0),
        c_uint32(len(atqb)),
        atqb))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_Set15693InitParameters(data_rate: VicinityDataRate,
                               sub_carrier: VicinitySubCarrier) -> None:
    """Initializes Vicinity simulation parameters

    Parameters
    ----------
    data_rate : VicinityDataRate
        VICC data rate
    sub_carrier : VicinitySubCarrier
        Number of VICC sub-carriers
    """
    if not isinstance(data_rate, VicinityDataRate):
        raise TypeError('data_rate must be an instance of '
                        'VicinityDataRate IntEnum')
    if not isinstance(sub_carrier, VicinitySubCarrier):
        raise TypeError('sub_carrier must be an instance of '
                        'VicinitySubCarrier IntEnum')
    ret = CTS3ErrorCode(_MPuLib.MPC_Set15693InitParameters(
        c_uint8(0),
        c_uint8(data_rate),
        c_uint8(sub_carrier)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SetNFCInitParameters(mode: NfcMode, data_rate: NfcDataRate,
                             masked_events: NfcSimulatorEvent,
                             sens_res: bytes, sel_res: Union[bytes, int],
                             nfc_id: bytes, atr_res: bytes) -> None:
    """Initializes NFC simulation parameters

    Parameters
    ----------
    mode : NfcMode
        NFC mode
    data_rate : NfcDataRate
        NFC data rate
    masked_events : NfcSimulatorEvent
        Mask of events ignored by simulator
    sens_res : bytes
        2-byte SENS_RES to answer
    sel_res : bytes or int
        SEL_RES byte to answer
    nfc_id : bytes
        NFCID1 to answer
    atr_res : bytes
        ATR_RES to answer
    """
    if not isinstance(mode, NfcMode):
        raise TypeError('mode must be an instance of NfcMode IntEnum')
    if not isinstance(data_rate, NfcDataRate):
        raise TypeError('data_rate must be an instance of NfcDataRate IntEnum')
    if not isinstance(masked_events, NfcSimulatorEvent):
        raise TypeError('masked_events must be an instance of '
                        'NfcSimulatorEvent IntFlag')
    if not isinstance(sens_res, bytes) or len(sens_res) != 2:
        raise TypeError('sens_res must be an instance of 2 bytes')
    if isinstance(sel_res, bytes):
        if len(sel_res) != 1:
            raise TypeError('sel_res must be an instance of 1 byte')
        sel_res_value = sel_res[0]
    elif isinstance(sel_res, int):
        _check_limits(c_uint8, sel_res, 'sel_res')
        sel_res_value = sel_res
    else:
        raise TypeError('sel_res must be an instance of int or 1 byte')
    if not isinstance(nfc_id, bytes):
        raise TypeError('nfc_id must be an instance of bytes')
    _check_limits(c_uint32, len(nfc_id), 'nfc_id')
    if not isinstance(atr_res, bytes):
        raise TypeError('atr_res must be an instance of bytes')
    _check_limits(c_uint32, len(atr_res), 'atr_res')
    ret = CTS3ErrorCode(_MPuLib.MPC_SetNFCInitParameters(
        c_uint8(0),
        c_uint8(mode),
        c_uint16(data_rate),
        c_uint32(masked_events),
        sens_res,
        byref(c_uint8(sel_res_value)),
        c_uint32(len(nfc_id)),
        nfc_id,
        c_uint32(len(atr_res)),
        atr_res))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SetSParameterInit(pcd_to_picc_bitrate: Union[bytes, int],
                          picc_to_pcd_bitrate: Union[bytes, int],
                          framing_option_picc_to_pcd: Union[bytes, int]) \
                         -> None:
    """Initializes S(PARAMETERS) blocks answer

    Parameters
    ----------
    pcd_to_picc_bitrate : bytes or int
        'Supported bit rates from PCD to PICC' byte value
    picc_to_pcd_bitrate : bytes or int
        'Supported bit rates from PICC to PCD' byte value
    framing_option_picc_to_pcd : bytes or int
        'Supported framing options from PICC to PCD' byte value
    """
    if isinstance(pcd_to_picc_bitrate, bytes):
        if len(pcd_to_picc_bitrate) != 1:
            raise TypeError('pcd_to_picc_bitrate must be an instance of '
                            '1 byte')
        pcd_to_picc = pcd_to_picc_bitrate[0]
    elif isinstance(pcd_to_picc_bitrate, int):
        _check_limits(c_uint8, pcd_to_picc_bitrate, 'pcd_to_picc_bitrate')
        pcd_to_picc = pcd_to_picc_bitrate
    else:
        raise TypeError('pcd_to_picc_bitrate must be an instance of '
                        'int or 1 byte')
    if isinstance(picc_to_pcd_bitrate, bytes):
        if len(picc_to_pcd_bitrate) != 1:
            raise TypeError('picc_to_pcd_bitrate must be an instance of '
                            '1 byte')
        picc_to_pcd = picc_to_pcd_bitrate[0]
    elif isinstance(picc_to_pcd_bitrate, int):
        _check_limits(c_uint8, picc_to_pcd_bitrate, 'picc_to_pcd_bitrate')
        picc_to_pcd = picc_to_pcd_bitrate
    else:
        raise TypeError('picc_to_pcd_bitrate must be an instance of '
                        'int or 1 byte')
    if isinstance(framing_option_picc_to_pcd, bytes):
        if len(framing_option_picc_to_pcd) != 1:
            raise TypeError('framing_option_picc_to_pcd must be an instance '
                            'of 1 byte')
        framing = framing_option_picc_to_pcd[0]
    elif isinstance(framing_option_picc_to_pcd, int):
        _check_limits(c_uint8, framing_option_picc_to_pcd,
                      'framing_option_picc_to_pcd')
        framing = framing_option_picc_to_pcd
    else:
        raise TypeError('framing_option_picc_to_pcd must be an instance of '
                        'int or 1 byte')

    ret = CTS3ErrorCode(_MPuLib.MPC_SetSParameterInit(
        c_uint8(0),
        c_uint8(pcd_to_picc),
        c_uint8(picc_to_pcd),
        c_uint8(framing),
        c_uint8(0),
        c_uint8(0)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)

# endregion

# region Frames reception


class _TypeARATSStruct(Structure):
    """RATS"""
    _fields_ = [('sb', c_uint8),
                ('param', c_uint8),
                ('crc_1', c_uint8),
                ('crc_2', c_uint8)]

    def get_bytes(self) -> bytes:
        """Converts RATS into bytes

        Returns
        -------
        bytes
            Bytes representation of RATS
        """
        return bytes([self.sb, self.param, self.crc_1, self.crc_2])


def MPC_GetRATS() -> bytes:
    """Gets RATS command

    Returns
    -------
    bytes
        RATS command
    """
    rats = _TypeARATSStruct()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetRATS(
        c_uint8(0),
        byref(rats)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return rats.get_bytes()


def MPC_GetATTRIB() -> bytes:
    """Gets ATTRIB command

    Returns
    -------
    bytes
        ATTRIB command
    """
    attrib = bytes(64)
    length = c_uint32()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetATTRIB(
        c_uint8(0),
        attrib,
        byref(length)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return attrib[:length.value]


def MPC_GetSParam() -> bytes:
    """Gets S(PARAMETERS) request

    Returns
    -------
    bytes
        S(PARAMETERS) request
    """
    s_param = bytes(64)
    length = c_uint32()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetSParam(
        c_uint8(0),
        s_param,
        byref(length)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return s_param[:length.value]


def MPC_GetBufferedRawFrame() -> Optional[Dict[str,
                                               Union[bytes, TechnologyType]]]:
    """Gets received frame

    Returns
    -------
    dict
        'rx_frame' (bytes): Received frame
        'rx_type' (TechnologyType): Received frame type
    """
    max_size = 65538
    data = bytes(max_size)
    rx_size = c_uint32()
    rx_type = c_int32()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetBufferedRawFrame(
        c_uint8(0),
        byref(rx_type),
        data,
        byref(rx_size)))
    if ret == CTS3ErrorCode.ERRSIM_NO_FRAME_AVAILABLE:
        return None
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return {'rx_frame': data[:rx_size.value],
            'rx_type': TechnologyType(rx_type.value)}


class _APDUHeader(Structure):
    """APDU header"""
    _fields_ = [('cla', c_uint8),
                ('ins', c_uint8),
                ('p1', c_uint8),
                ('p2', c_uint8),
                ('p3', c_uint8)]

    def get_bytes(self) -> bytes:
        """Converts APDU header into bytes

        Returns
        -------
        bytes
            Bytes representation of APDU header
        """
        return bytes([self.cla, self.ins, self.p1, self.p2, self.p3])


def MPS_GetAPDU2() -> Dict[str, bytes]:
    """Gets APDU request

    Returns
    -------
    dict
        'header' (bytes): APDU header
        'data' (bytes): APDU data
    """
    header = _APDUHeader()
    data = bytes(0xFFFF)
    length = c_uint32()
    apdu_len = c_uint32()
    ret = CTS3ErrorCode(_MPuLib.MPS_GetAPDU2(
        c_uint8(0),
        byref(header),
        data,
        byref(length),
        byref(apdu_len)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return {'header': header.get_bytes()[:apdu_len.value - length.value],
            'data': data[:length.value]}


class _TypeNFC_ATR_REQ(Structure):
    """ATR_REQ"""
    _fields_ = [('nfc_id3i', c_uint8 * 10),
                ('didi', c_uint8),
                ('bsi', c_uint8),
                ('bri', c_uint8),
                ('ppi', c_uint8),
                ('general_bytes', c_uint8 * 238)]

    def get_bytes(self, length: int) -> bytes:
        """Converts ATR_REQ into bytes

        Returns
        -------
        bytes
            Bytes representation of ATR_REQ
        """
        return bytes(list(self.nfc_id3i) + [self.didi, self.bsi, self.bri] +
                     self.general_bytes[:length-12])


def MPC_GetNFC_ATR_REQ() -> bytes:
    """Gets ATR_REQ request

    Returns
    -------
    bytes
        ATR_REQ request
    """
    atr_req = _TypeNFC_ATR_REQ()
    length = c_uint16()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetNFC_ATR_REQ(
        c_uint8(0),
        byref(length),
        byref(atr_req)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return atr_req.get_bytes(length.value)


class _TypeNFC_PSL_REQ(Structure):
    """PSL_REQ"""
    _fields_ = [('did', c_uint8),
                ('brs', c_uint8),
                ('fsl', c_uint8)]

    def get_bytes(self) -> bytes:
        """Converts PSL_REQ into bytes

        Returns
        -------
        bytes
            Bytes representation of PSL_REQ
        """
        return bytes([self.did, self.brs, self.fsl])


def MPC_GetNFC_PSL_REQ() -> bytes:
    """Gets PSL_REQ request

    Returns
    -------
    bytes
        PSL_REQ request
    """
    psl_req = _TypeNFC_PSL_REQ()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetNFC_PSL_REQ(
        c_uint8(0),
        byref(psl_req)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return psl_req.get_bytes()


class _TypeNFC_WUP_REQ(Structure):
    """WUP_REQ"""
    _fields_ = [('nfc_id3i', c_uint8 * 10),
                ('didi', c_uint8)]

    def get_bytes(self) -> bytes:
        """Converts WUP_REQ into bytes

        Returns
        -------
        bytes
            Bytes representation of WUP_REQ
        """
        return bytes(list(self.nfc_id3i) + [self.didi])


def MPC_GetNFC_WUP_REQ() -> bytes:
    """Gets WUP_REQ request

    Returns
    -------
    bytes
        WUP_REQ request
    """
    wup_req = _TypeNFC_WUP_REQ()
    length = c_uint16()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetNFC_WUP_REQ(
        c_uint8(0),
        byref(length),
        byref(wup_req)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return wup_req.get_bytes()


def MPC_GetNFC_DEP_REQ() -> bytes:
    """Gets DEP_REQ request

    Returns
    -------
    bytes
        DEP_REQ request
    """
    dep_req = bytes(0xFFFF)
    length = c_uint32()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetNFC_DEP_REQ(
        c_uint8(0),
        byref(length),
        dep_req))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return dep_req[:length.value]


def MPC_GetNFC_UserData() -> bytes:
    """Gets NFC user data over DEP_REQ protocol

    Returns
    -------
    bytes
        User data
    """
    data = bytes(0xFFFF)
    length = c_uint32()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetNFC_UserData(
        c_uint8(0),
        byref(length),
        data))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return data[:length.value]


class _TypeAPPSStruct(Structure):
    """PPS request"""
    _fields_ = [('ppss', c_uint8),
                ('pps0', c_uint8),
                ('pps1', c_uint8),
                ('crc1', c_uint8),
                ('crc2', c_uint8)]

    def get_bytes(self) -> bytes:
        """Converts PPS into bytes

        Returns
        -------
        bytes
            Bytes representation of PPS
        """
        return bytes([self.ppss, self.pps0, self.pps1, self.crc1, self.crc2])


def MPC_GetPPSRequest() -> bytes:
    """Gets Type A PPS request

    Returns
    -------
    bytes
        PPS request
    """
    pps = _TypeAPPSStruct()
    ret = CTS3ErrorCode(_MPuLib.MPC_GetPPSRequest(
        c_uint8(0),
        byref(pps)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    return pps.get_bytes()


# endregion

# region Frames transmission


def MPS_SendRAPDU(apdu: bytes, status: Union[int, bytes]) -> None:
    """Sends response APDU

    Parameters
    ----------
    apdu : bytes
        Response APDU
    status : int or bytes
        2-byte status word
    """
    if not isinstance(apdu, bytes):
        raise TypeError('apdu must be an instance of bytes')
    if isinstance(status, bytes):
        if len(status) != 2:
            raise TypeError('status must be an instance of 2 bytes')
        status_word = status[0] << 8
        status_word |= status[1]
    elif isinstance(status, int):
        _check_limits(c_uint16, status, 'status')
        status_word = status
    else:
        raise TypeError('status must be an instance of int or 2 bytes')
    ret = CTS3ErrorCode(_MPuLib.MPS_SendRAPDU(
        c_uint8(0),
        apdu,
        c_uint32(len(apdu)),
        c_uint16(status_word)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendNFC_PSL_RES(did: Union[int, bytes] = 0xFF,
                        crc: Union[int, bytes] = 0) -> None:
    """Sends PSL_RES response

    Parameters
    ----------
    did : int or bytes, optional
        1-byte DID
    crc : int or bytes, optional
        2-byte CRC
    """
    if isinstance(did, bytes):
        if len(did) != 1:
            raise TypeError('did must be an instance of 1 byte')
        did_value = did[0]
    elif isinstance(did, int):
        _check_limits(c_uint8, did, 'did')
        did_value = did
    else:
        raise TypeError('did must be an instance of int or 1 byte')
    if isinstance(crc, bytes):
        if len(crc) != 2:
            raise TypeError('crc must be an instance of 2 bytes')
        crc_value = crc[0] << 8
        crc_value |= crc[1]
    elif isinstance(crc, int):
        _check_limits(c_uint16, crc, 'crc')
        crc_value = crc
    else:
        raise TypeError('crc must be an instance of int or 2 bytes')
    ret = CTS3ErrorCode(_MPuLib.MPC_SendNFC_PSL_RES(
        c_uint8(0),
        byref(c_uint8(did_value)),
        byref(c_uint16(crc_value))))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendNFC_DSL_RES(did: Union[int, bytes] = 0xFF,
                        crc: Union[int, bytes] = 0) -> None:
    """Sends DSL_RES response

    Parameters
    ----------
    did : int or bytes, optional
        1-byte DID
    crc : int or bytes, optional
        2-byte CRC
    """
    if isinstance(did, bytes):
        if len(did) != 1:
            raise TypeError('did must be an instance of 1 byte')
        did_value = did[0]
    elif isinstance(did, int):
        _check_limits(c_uint8, did, 'did')
        did_value = did
    else:
        raise TypeError('did must be an instance of int or 1 byte')
    if isinstance(crc, bytes):
        if len(crc) != 2:
            raise TypeError('crc must be an instance of 2 bytes')
        crc_value = crc[0] << 8
        crc_value |= crc[1]
    elif isinstance(crc, int):
        _check_limits(c_uint16, crc, 'crc')
        crc_value = crc
    else:
        raise TypeError('crc must be an instance of int or 2 bytes')
    ret = CTS3ErrorCode(_MPuLib.MPC_SendNFC_DSL_RES(
        c_uint8(0),
        byref(c_uint8(did_value)),
        byref(c_uint16(crc_value))))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendNFC_RLS_RES(did: Union[int, bytes] = 0xFF,
                        crc: Union[int, bytes] = 0) -> None:
    """Sends RLS_RES response

    Parameters
    ----------
    did : int or bytes, optional
        1-byte DID
    crc : int or bytes, optional
        2-byte CRC
    """
    if isinstance(did, bytes):
        if len(did) != 1:
            raise TypeError('did must be an instance of 1 byte')
        did_value = did[0]
    elif isinstance(did, int):
        _check_limits(c_uint8, did, 'did')
        did_value = did
    else:
        raise TypeError('did must be an instance of int or 1 byte')
    if isinstance(crc, bytes):
        if len(crc) != 2:
            raise TypeError('crc must be an instance of 2 bytes')
        crc_value = crc[0] << 8
        crc_value |= crc[1]
    elif isinstance(crc, int):
        _check_limits(c_uint16, crc, 'crc')
        crc_value = crc
    else:
        raise TypeError('crc must be an instance of int or 2 bytes')
    ret = CTS3ErrorCode(_MPuLib.MPC_SendNFC_RLS_RES(
        c_uint8(0),
        byref(c_uint8(did_value)),
        byref(c_uint16(crc_value))))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendNFC_WUP_RES(did: Union[int, bytes] = 0xFF,
                        crc: Union[int, bytes] = 0) -> None:
    """Sends WUP_RES response

    Parameters
    ----------
    did : int or bytes, optional
        1-byte DID
    crc : int or bytes, optional
        2-byte CRC
    """
    if isinstance(did, bytes):
        if len(did) != 1:
            raise TypeError('did must be an instance of 1 byte')
        did_value = did[0]
    elif isinstance(did, int):
        _check_limits(c_uint8, did, 'did')
        did_value = did
    else:
        raise TypeError('did must be an instance of int or 1 byte')
    if isinstance(crc, bytes):
        if len(crc) != 2:
            raise TypeError('crc must be an instance of 2 bytes')
        crc_value = crc[0] << 8
        crc_value |= crc[1]
    elif isinstance(crc, int):
        _check_limits(c_uint16, crc, 'crc')
        crc_value = crc
    else:
        raise TypeError('crc must be an instance of int or 2 bytes')
    ret = CTS3ErrorCode(_MPuLib.MPC_SendNFC_WUP_RES(
        c_uint8(0),
        byref(c_uint8(did_value)),
        byref(c_uint16(crc_value))))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendNFCTimeoutExtensionRequest(rtox: Union[int, bytes]) -> None:
    """Sends Response Timeout Extension PDU

    Parameters
    ----------
    rtox : int or bytes
        1-byte RTOX value
    """
    if isinstance(rtox, bytes):
        if len(rtox) != 1:
            raise TypeError('rtox must be an instance of 1 byte')
        rtox_value = rtox[0]
    elif isinstance(rtox, int):
        _check_limits(c_uint8, rtox, 'rtox')
        rtox_value = rtox
    else:
        raise TypeError('rtox must be an instance of int or 1 byte')
    ret = CTS3ErrorCode(_MPuLib.MPC_SendNFCTimeoutExtensionRequest(
        c_uint8(0),
        c_uint8(rtox_value)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendNFC_DEP_RES(pfb: Union[int, bytes],
                        data: Optional[bytes],
                        did: Union[int, bytes] = 0xFF,
                        nad: Union[int, bytes] = 0xFF,
                        crc: Union[int, bytes] = 0) -> None:
    """Sends DEP_RES response

    Parameters
    ----------
    pfb : int or bytes
        1-byte RTOX value
    data : bytes
        User data
    did : int or bytes, optional
        1-byte DID
    nad : int or bytes, optional
        1-byte DID
    crc : int or bytes, optional
        2-byte CRC
    """
    if isinstance(pfb, bytes):
        if len(pfb) != 1:
            raise TypeError('pfb must be an instance of 1 byte')
        pfb_value = pfb[0]
    elif isinstance(pfb, int):
        _check_limits(c_uint8, pfb, 'pfb')
        pfb_value = pfb
    else:
        raise TypeError('pfb must be an instance of int or 1 byte')
    if data is not None and data is not isinstance(data, bytes):
        raise TypeError('data must be an instance of bytes')
    if isinstance(did, bytes):
        if len(did) != 1:
            raise TypeError('did must be an instance of 1 byte')
        did_value = did[0]
    elif isinstance(did, int):
        _check_limits(c_uint8, did, 'did')
        did_value = did
    else:
        raise TypeError('did must be an instance of int or 1 byte')
    if isinstance(nad, bytes):
        if len(nad) != 1:
            raise TypeError('nad must be an instance of 1 byte')
        nad_value = nad[0]
    elif isinstance(nad, int):
        _check_limits(c_uint8, nad, 'nad')
        nad_value = nad
    else:
        raise TypeError('nad must be an instance of int or 1 byte')
    if isinstance(crc, bytes):
        if len(crc) != 2:
            raise TypeError('crc must be an instance of 2 bytes')
        crc_value = crc[0] << 8
        crc_value |= crc[1]
    elif isinstance(crc, int):
        _check_limits(c_uint16, crc, 'crc')
        crc_value = crc
    else:
        raise TypeError('crc must be an instance of int or 2 bytes')
    ret = CTS3ErrorCode(_MPuLib.MPC_SendNFC_DEP_RES(
        c_uint8(0),
        c_uint8(pfb_value),
        c_uint32(0) if data is None else c_uint32(len(data)),
        data,
        byref(c_uint8(did_value)),
        byref(c_uint8(nad_value)),
        byref(c_uint16(crc_value))))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendNFC_RUserData(data: bytes) -> None:
    """Sends data using DEP_REQ protocol

    Parameters
    ----------
    data : bytes
        Data to send
    """
    if not isinstance(data, bytes):
        raise TypeError('data must be an instance of bytes')
    ret = CTS3ErrorCode(_MPuLib.MPC_SendNFC_RUserData(
        c_uint8(0),
        c_uint32(len(data)),
        data))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPC_SendPPSResponse(pps: bytes = None) -> None:
    """Sends Type A PPS response

    Parameters
    ----------
    pps : bytes, optional
        5-byte PPS response
    """
    if pps is None:
        ret = CTS3ErrorCode(_MPuLib.MPC_GetPPSRequest(
            c_uint8(0),
            None))
    else:
        if not isinstance(pps, bytes) or len(pps) != 5:
            raise TypeError('pps must be an instance of 5 bytes')
        pps_struct = _TypeAPPSStruct(pps[0], pps[1], pps[2], pps[3], pps[4])
        ret = CTS3ErrorCode(_MPuLib.MPC_GetPPSRequest(
            c_uint8(0),
            byref(pps_struct)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


@unique
class WtxRequestMode(IntEnum):
    """S(WTX) request mode"""
    WTX_BWT_MULT = 1
    WTX_ETU = 2
    WTX_MS = 3


def MPS_SendWTXRequest(unit: WtxRequestMode, value: int) -> None:
    """Sends S(WTX) request

    Parameters
    ----------
    unit : WtxRequestMode
        S(WTX) request unit
    value : int
        S(WTX) request value
    """
    if not isinstance(unit, WtxRequestMode):
        raise TypeError('unit must be an instance of WtxRequestMode IntEnum')
    _check_limits(c_uint32, value, 'value')
    ret = CTS3ErrorCode(_MPuLib.MPS_SendWTXRequest(
        c_uint8(0),
        c_uint8(unit),
        c_uint32(value)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)

# endregion

# region Simulator management


@unique
class _SimulatorProtocol(IntEnum):
    """Simulation protocols"""
    CL_14443_SIMULATOR = 1 << 16
    CL_FELICA_SIMULATOR = 1 << 17
    CL_VICINITY_SIMULATOR = 1 << 18
    CL_NFC_SIMULATOR = 1 << 19
    CL_TAG_TYPE2_SIMULATOR = 1 << 20


def MPS_SimWaitNStart(event_mask: Union[IsoSimulatorEvent,
                                        FeliCaSimulatorEvent,
                                        VicinitySimulatorEvent,
                                        NfcSimulatorEvent,
                                        Type2TagSimulatorEvent],
                      start_spy: bool, timeout: float) -> None:
    """Starts simulator

    Parameters
    ----------
    event_mask : IsoSimulatorEvent, Type2TagSimulatorEvent, \
                 FeliCaSimulatorEvent, VicinitySimulatorEvent \
                 or NfcSimulatorEvent
        Enabled events
    start_spy : bool
        True to start protocol analyzer
    timeout : float
        RF field detection timeout in s
    """
    if isinstance(event_mask, IsoSimulatorEvent):
        protocol = _SimulatorProtocol.CL_14443_SIMULATOR
    elif isinstance(event_mask, FeliCaSimulatorEvent):
        protocol = _SimulatorProtocol.CL_FELICA_SIMULATOR
    elif isinstance(event_mask, VicinitySimulatorEvent):
        protocol = _SimulatorProtocol.CL_VICINITY_SIMULATOR
    elif isinstance(event_mask, NfcSimulatorEvent):
        protocol = _SimulatorProtocol.CL_NFC_SIMULATOR
    elif isinstance(event_mask, Type2TagSimulatorEvent):
        protocol = _SimulatorProtocol.CL_TAG_TYPE2_SIMULATOR
    else:
        raise TypeError('event_mask must be an instance of '
                        'IsoSimulatorEvent IntFlag, '
                        'FeliCaSimulatorEvent IntFlag, '
                        'VicinitySimulatorEvent IntFlag, '
                        'NfcSimulatorEvent IntFlag or '
                        'Type2TagSimulatorEvent IntFlag')
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    ret = CTS3ErrorCode(_MPuLib.MPS_SimWaitNStart(
        c_uint8(0),
        c_uint32(protocol),
        c_uint32(event_mask),
        c_uint8(1) if start_spy else c_uint8(0),
        c_uint32(timeout_ms)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPS_SimStop() -> None:
    """Stops simulator"""
    ret = CTS3ErrorCode(_MPuLib.MPS_SimStop(
        c_uint8(0),
        c_uint32(0)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPS_WaitSimEvent(timeout: float) -> Union[None,
                                              IsoSimulatorEvent,
                                              FeliCaSimulatorEvent,
                                              VicinitySimulatorEvent,
                                              NfcSimulatorEvent,
                                              Type2TagSimulatorEvent]:
    """Waits for a simulator event

    Parameters
    ----------
    timeout : float
        Event timeout in s

    Returns
    -------
    IsoSimulatorEvent, FeliCaSimulatorEvent, VicinitySimulatorEvent, \
            NfcSimulatorEvent or Type2TagSimulatorEvent
        Received event
    """
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    protocol = c_uint32()
    event = c_uint32()
    ret = CTS3ErrorCode(_MPuLib.MPS_WaitSimEvent(
        c_uint8(0),
        c_uint32(timeout_ms),
        c_uint32(0),
        byref(event),
        byref(protocol)))
    if ret == CTS3ErrorCode.CRET_SIM_NO_EVENT:
        return None
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)
    if protocol.value == _SimulatorProtocol.CL_14443_SIMULATOR:
        return IsoSimulatorEvent(event.value)
    elif protocol.value == _SimulatorProtocol.CL_FELICA_SIMULATOR:
        return FeliCaSimulatorEvent(event.value)
    elif protocol.value == _SimulatorProtocol.CL_VICINITY_SIMULATOR:
        return VicinitySimulatorEvent(event.value)
    elif protocol.value == _SimulatorProtocol.CL_NFC_SIMULATOR:
        return NfcSimulatorEvent(event.value)
    else:
        return Type2TagSimulatorEvent(event.value)


@unique
class SimulatorParameter(IntEnum):
    """Simulator parameters"""
    SIM_SET_EVENTS_MASK = 5
    SIM_SET_AUTO_WTX = 20
    SIM_SET_MUTE_INITRULE_ON = 21
    SIM_SET_MUTE_INITRULE_OFF = 22
    SIM_SET_ATS_CRC_FORCED = 23
    SIM_SET_ATS_CRC_AUTO = 24
    SIM_SET_AUTO_WTX_VALUE = 25
    SIM_SET_STRICT_RFU_CHECKING = 26
    SIM_SET_ATR_RES_CRC_FORCED = 27
    SIM_SET_ATR_RES_CRC_AUTO = 28
    SIM_SET_WUP_RES_CRC_FORCED = 29
    SIM_SET_WUP_RES_CRC_AUTO = 30
    SIM_SET_POLL_RES_CRC_FORCED = 31
    SIM_SET_POLL_RES_CRC_AUTO = 32
    SIM_SET_NFC_MAX_SUCCESSIVE_NAK = 35
    SIM_SET_NFC_MAX_SUCCESSIVE_ATTENTION = 36


def MPS_SetSimParameter(param_type: SimulatorParameter,
                        value: int) -> None:
    """Changes simulator parameter

    Parameters
    ----------
    param_type : SimulatorParameter
        Parameter type
    value : int
        Parameter value
    """
    if not isinstance(param_type, SimulatorParameter):
        raise TypeError('param_type must be an instance of '
                        'SimulatorParameter IntEnum')
    _check_limits(c_uint32, value, 'value')
    ret = CTS3ErrorCode(_MPuLib.MPS_SetSimParameter(
        c_uint8(0),
        c_uint32(param_type),
        byref(c_uint32(value)),
        c_uint32(4)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPS_DefaultProtocolProc(event: Union[IsoSimulatorEvent,
                                         FeliCaSimulatorEvent,
                                         VicinitySimulatorEvent,
                                         NfcSimulatorEvent,
                                         Type2TagSimulatorEvent]) -> None:
    """Runs default action for the specified event

    Parameters
    ----------
    event : IsoSimulatorEvent, Type2TagSimulatorEvent, \
            FeliCaSimulatorEvent, VicinitySimulatorEvent \
            or NfcSimulatorEvent
        Event which will trigger default action
    """
    if isinstance(event, IsoSimulatorEvent):
        protocol = _SimulatorProtocol.CL_14443_SIMULATOR
    elif isinstance(event, FeliCaSimulatorEvent):
        protocol = _SimulatorProtocol.CL_FELICA_SIMULATOR
    elif isinstance(event, VicinitySimulatorEvent):
        protocol = _SimulatorProtocol.CL_VICINITY_SIMULATOR
    elif isinstance(event, NfcSimulatorEvent):
        protocol = _SimulatorProtocol.CL_NFC_SIMULATOR
    elif isinstance(event, Type2TagSimulatorEvent):
        protocol = _SimulatorProtocol.CL_TAG_TYPE2_SIMULATOR
    else:
        raise TypeError('event must be an instance of '
                        'IsoSimulatorEvent IntFlag, '
                        'FeliCaSimulatorEvent IntFlag, '
                        'VicinitySimulatorEvent IntFlag, '
                        'NfcSimulatorEvent IntFlag or '
                        'Type2TagSimulatorEvent IntFlag')
    ret = CTS3ErrorCode(_MPuLib.MPS_DefaultProtocolProc(
        c_uint8(0),
        c_uint32(protocol),
        c_uint32(event)))
    if ret != CTS3ErrorCode.RET_OK:
        raise CTS3Exception(ret)


def MPS_GetLastError() -> CTS3ErrorCode:
    """Gets error code associated to SIM_EVT_CL_NFC_ERROR event

    Returns
    -------
    CTS3ErrorCode
        Error code
    """
    return CTS3ErrorCode(_MPuLib.MPS_GetLastError(
        c_uint8(0)))

# endregion

# region Rules management

# endregion

# region Filters management

# endregion
