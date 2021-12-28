from datetime import datetime
import pathlib
import socket
import logging
import abc
import ftplib
from madrigalWeb import madrigalWeb


logger = logging.getLogger(__name__)


class Downloader(abc.ABC):
    
    def __init__(self, base_dir: pathlib.Path, *args, **kwargs):
        logger.info(f"initializing {self.__class__}")
        self.base_dir = pathlib.Path(base_dir)

    @abc.abstractmethod
    def download(self, start_date: datetime, end_date: datetime):
        ...


class MadrigalTecDownloader(Downloader):

    def __init__(self, base_dir, user_name, user_email, user_affil):
        super().__init__(base_dir)
        self.dl_dir = self.base_dir / "madrigal_tec"
        self.dl_dir.mkdir(parents=True, exist_ok=True)
        self.user_name = user_name
        self.user_email = user_email
        self.user_affil = user_affil
        logger.info("connecting to server")
        self.server = madrigalWeb.MadrigalData("http://cedar.openmadrigal.org")

    def _get_tec_experiments(self, start_date: datetime, end_date: datetime):
        logger.info(f"getting TEC experiments between {start_date} and {end_date}")
        return self.server.getExperiments(
            8000,
            start_date.year, start_date.month, start_date.day, start_date.hour, start_date.minute, start_date.second,
            end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second,
        )

    def _download_file(self, tec_file, local_path):
        logger.info(f"downloading TEC file {tec_file.name} to {local_path}")
        try:
            return self.server.downloadFile(
                tec_file.name, str(local_path), self.user_name, self.user_email, self.user_affil, 'hdf5'
            )
        except socket.timeout:
            print(f'Failure downloading {tec_file.name} because it took more than allowed number of seconds')

    def download(self, start_date, end_date):
        tec_files = []
        experiments = sorted(self._get_tec_experiments(start_date, end_date))
        for experiment in experiments:
            experiment_files = self.server.getExperimentFiles(experiment.id)
            tec_file = next(filter(lambda exp: exp.kindat == 3500, experiment_files))
            tec_files.append(tec_file)
        print(f"{len(tec_files)} files being downloaded")
        for tec_file in tec_files:
            server_path = pathlib.Path(tec_file.name)
            local_path = self.dl_dir / f"{server_path.stem}.hdf5"
            self._download_file(tec_file, local_path)


class AuroralBoundaryDownloader(Downloader):

    def __init__(self, base_dir):
        super().__init__(base_dir)
        self.dl_dir = self.base_dir / "auroral_boundary"
        self.dl_dir.mkdir(parents=True, exist_ok=True)
        logger.info("connecting to server")
        self.server = ftplib.FTP_TLS("spdf.gsfc.nasa.gov")

    def download(self, start_date, end_date):
        ...


class OmniDownloader(Downloader):

    def __init__(self, base_dir):
        super().__init__(base_dir)
        self.dl_dir = self.base_dir / "omni"
        self.dl_dir.mkdir(parents=True, exist_ok=True)
        logger.info("connecting to server")
        self.server = ftplib.FTP_TLS("spdf.gsfc.nasa.gov")

    def download(self, start_date, end_date):
        ...
