"""Modalities"""

from enum import IntEnum
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema_models.pid_names import BaseName


class ModalityModel(BaseName):
    """Base model for modality"""

    model_config = ConfigDict(frozen=True)
    name: str
    abbreviation: str


class _Behavior(ModalityModel):
    """Model behavior"""

    name: Literal["Behavior"] = "Behavior"
    abbreviation: Literal["behavior"] = "behavior"


class _Behavior_Videos(ModalityModel):
    """Model behavior-videos"""

    name: Literal["Behavior videos"] = "Behavior videos"
    abbreviation: Literal["behavior-videos"] = "behavior-videos"


class _Confocal(ModalityModel):
    """Model confocal"""

    name: Literal["Confocal microscopy"] = "Confocal microscopy"
    abbreviation: Literal["confocal"] = "confocal"


class _Emg(ModalityModel):
    """Model EMG"""

    name: Literal["Electromyography"] = "Electromyography"
    abbreviation: Literal["EMG"] = "EMG"


class _Ecephys(ModalityModel):
    """Model ecephys"""

    name: Literal["Extracellular electrophysiology"] = "Extracellular electrophysiology"
    abbreviation: Literal["ecephys"] = "ecephys"


class _Fib(ModalityModel):
    """Model fib"""

    name: Literal["Fiber photometry"] = "Fiber photometry"
    abbreviation: Literal["fib"] = "fib"


class _Fmost(ModalityModel):
    """Model fMOST"""

    name: Literal["Fluorescence micro-optical sectioning tomography"] = (
        "Fluorescence micro-optical sectioning tomography"
    )
    abbreviation: Literal["fMOST"] = "fMOST"


class _Icephys(ModalityModel):
    """Model icephys"""

    name: Literal["Intracellular electrophysiology"] = "Intracellular electrophysiology"
    abbreviation: Literal["icephys"] = "icephys"


class _Isi(ModalityModel):
    """Model ISI"""

    name: Literal["Intrinsic signal imaging"] = "Intrinsic signal imaging"
    abbreviation: Literal["ISI"] = "ISI"


class _Mri(ModalityModel):
    """Model MRI"""

    name: Literal["Magnetic resonance imaging"] = "Magnetic resonance imaging"
    abbreviation: Literal["MRI"] = "MRI"


class _Merfish(ModalityModel):
    """Model merfish"""

    name: Literal["Multiplexed error-robust fluorescence in situ hybridization"] = (
        "Multiplexed error-robust fluorescence in situ hybridization"
    )
    abbreviation: Literal["merfish"] = "merfish"


class _Pophys(ModalityModel):
    """Model pophys"""

    name: Literal["Planar optical physiology"] = "Planar optical physiology"
    abbreviation: Literal["pophys"] = "pophys"


class _Slap(ModalityModel):
    """Model slap"""

    name: Literal["Scanned line projection imaging"] = "Scanned line projection imaging"
    abbreviation: Literal["slap"] = "slap"


class _Spim(ModalityModel):
    """Model SPIM"""

    name: Literal["Selective plane illumination microscopy"] = "Selective plane illumination microscopy"
    abbreviation: Literal["SPIM"] = "SPIM"


class Modality:
    """Modalities"""

    BEHAVIOR = _Behavior()
    BEHAVIOR_VIDEOS = _Behavior_Videos()
    CONFOCAL = _Confocal()
    EMG = _Emg()
    ECEPHYS = _Ecephys()
    FIB = _Fib()
    FMOST = _Fmost()
    ICEPHYS = _Icephys()
    ISI = _Isi()
    MRI = _Mri()
    MERFISH = _Merfish()
    POPHYS = _Pophys()
    SLAP = _Slap()
    SPIM = _Spim()

    ALL = tuple(ModalityModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(ModalityModel.__subclasses__())], Field(discriminator="abbreviation")]

    abbreviation_map = {m().abbreviation: m() for m in ALL}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        """Get modality from abbreviation"""
        return cls.abbreviation_map.get(abbreviation, None)


class FileRequirement(IntEnum):
    """Whether a file is required for a specific modality"""

    REQUIRED = 1
    OPTIONAL = 0
    EXCLUDED = -1


class ExpectedFilesModel(BaseModel):
    """Base model for modality"""

    model_config = ConfigDict(frozen=True)
    name: str
    modality_abbreviation: str
    subject: FileRequirement
    data_description: FileRequirement
    procedures: FileRequirement
    processing: FileRequirement
    acquisition: FileRequirement
    instrument: FileRequirement
    quality_control: FileRequirement


class _Behavior_Files(ExpectedFilesModel):
    """Model behavior_Files"""

    name: Literal["Behavior"] = "Behavior"
    modality_abbreviation: Literal["behavior"] = "behavior"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Behavior_Videos_Files(ExpectedFilesModel):
    """Model behavior-videos_Files"""

    name: Literal["Behavior videos"] = "Behavior videos"
    modality_abbreviation: Literal["behavior-videos"] = "behavior-videos"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Confocal_Files(ExpectedFilesModel):
    """Model confocal_Files"""

    name: Literal["Confocal microscopy"] = "Confocal microscopy"
    modality_abbreviation: Literal["confocal"] = "confocal"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.REQUIRED
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Emg_Files(ExpectedFilesModel):
    """Model EMG_Files"""

    name: Literal["Electromyography"] = "Electromyography"
    modality_abbreviation: Literal["EMG"] = "EMG"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Ecephys_Files(ExpectedFilesModel):
    """Model ecephys_Files"""

    name: Literal["Extracellular electrophysiology"] = "Extracellular electrophysiology"
    modality_abbreviation: Literal["ecephys"] = "ecephys"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Fib_Files(ExpectedFilesModel):
    """Model fib_Files"""

    name: Literal["Fiber photometry"] = "Fiber photometry"
    modality_abbreviation: Literal["fib"] = "fib"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Fmost_Files(ExpectedFilesModel):
    """Model fMOST_Files"""

    name: Literal["Fluorescence micro-optical sectioning tomography"] = (
        "Fluorescence micro-optical sectioning tomography"
    )
    modality_abbreviation: Literal["fMOST"] = "fMOST"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.REQUIRED
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Icephys_Files(ExpectedFilesModel):
    """Model icephys_Files"""

    name: Literal["Intracellular electrophysiology"] = "Intracellular electrophysiology"
    modality_abbreviation: Literal["icephys"] = "icephys"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Isi_Files(ExpectedFilesModel):
    """Model ISI_Files"""

    name: Literal["Intrinsic signal imaging"] = "Intrinsic signal imaging"
    modality_abbreviation: Literal["ISI"] = "ISI"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Mri_Files(ExpectedFilesModel):
    """Model MRI_Files"""

    name: Literal["Magnetic resonance imaging"] = "Magnetic resonance imaging"
    modality_abbreviation: Literal["MRI"] = "MRI"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Merfish_Files(ExpectedFilesModel):
    """Model merfish_Files"""

    name: Literal["Multiplexed error-robust fluorescence in situ hybridization"] = (
        "Multiplexed error-robust fluorescence in situ hybridization"
    )
    modality_abbreviation: Literal["merfish"] = "merfish"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.REQUIRED
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Pophys_Files(ExpectedFilesModel):
    """Model pophys_Files"""

    name: Literal["Planar optical physiology"] = "Planar optical physiology"
    modality_abbreviation: Literal["pophys"] = "pophys"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Slap_Files(ExpectedFilesModel):
    """Model slap_Files"""

    name: Literal["Scanned line projection imaging"] = "Scanned line projection imaging"
    modality_abbreviation: Literal["slap"] = "slap"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.OPTIONAL
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class _Spim_Files(ExpectedFilesModel):
    """Model SPIM_Files"""

    name: Literal["Selective plane illumination microscopy"] = "Selective plane illumination microscopy"
    modality_abbreviation: Literal["SPIM"] = "SPIM"
    subject: FileRequirement = FileRequirement.REQUIRED
    data_description: FileRequirement = FileRequirement.REQUIRED
    procedures: FileRequirement = FileRequirement.REQUIRED
    processing: FileRequirement = FileRequirement.REQUIRED
    acquisition: FileRequirement = FileRequirement.REQUIRED
    instrument: FileRequirement = FileRequirement.REQUIRED
    quality_control: FileRequirement = FileRequirement.OPTIONAL


class ExpectedFiles:
    """Expected files for each modality"""

    BEHAVIOR = _Behavior_Files()
    BEHAVIOR_VIDEOS = _Behavior_Videos_Files()
    CONFOCAL = _Confocal_Files()
    EMG = _Emg_Files()
    ECEPHYS = _Ecephys_Files()
    FIB = _Fib_Files()
    FMOST = _Fmost_Files()
    ICEPHYS = _Icephys_Files()
    ISI = _Isi_Files()
    MRI = _Mri_Files()
    MERFISH = _Merfish_Files()
    POPHYS = _Pophys_Files()
    SLAP = _Slap_Files()
    SPIM = _Spim_Files()

    ALL = tuple(ExpectedFilesModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(ExpectedFilesModel.__subclasses__())], Field(discriminator="abbreviation")]
