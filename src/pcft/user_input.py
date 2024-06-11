from dataclasses import dataclass


"""
# Settings
AOI_FILENAME: str = '<YOUR AOI FILE HERE>'
CLOUD = 1
START_DATE = '2018'
END_DATE = '2021'
DEPENDENT: str = 'NDVI'
MODES: int = 4

"""


@dataclass
class UserInput:
    sensor_type: str
    aoi_file_name: str
    cloud_percent: float
    start_date: str
    end_date: str
    dependent: str
    modes: int


def get_user_input() -> UserInput:
    sensor_type = input("Enter Sensor: (S2/LS): ")
    aoi_file_name = input("Enter AOI Filename: ")
    cloud_percent = float(input("Enter Cloud Percent: "))
    start_date = input("Enter Start Year (YYYY): ")
    end_date = str(int(input("Enter End Year (YYYY): ")) + 1)
    dependend = input("Enter Dependent Variable (NDVI): ")
    n_modes = int(input("Enter Number of Modes: "))

    if dependend == "":
        dependend = "NDVI"

    input_obj = UserInput(
        sensor_type=sensor_type.lower().strip(),
        aoi_file_name=aoi_file_name,
        cloud_percent=cloud_percent,
        start_date=start_date,
        end_date=end_date,
        dependent=dependend,
        modes=n_modes,
    )

    return input_obj
