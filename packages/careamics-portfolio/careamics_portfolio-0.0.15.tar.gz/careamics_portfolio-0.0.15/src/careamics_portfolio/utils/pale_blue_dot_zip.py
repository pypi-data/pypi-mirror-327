from ..portfolio_entry import PortfolioEntry


class PaleBlueDotZip(PortfolioEntry):
    """The original Pale Blue Dot image.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio="test",
            name="PaleBlueDotZip",
            url="https://download.fht.org/jug/careamics/pale_blue_dot.zip",
            file_name="pale_blue_dot.zip",
            sha256="90b03ec7a9e1980fd112a40c2c935015bb349cdf89fbf3db78c715dd2a49db47",
            description="Pale Blue Dot, credit NASA/JPL-Caltech."
            "Original caption: This narrow-angle color image of the"
            " Earth, dubbed 'Pale Blue Dot', is a part of the first"
            " ever 'portrait' of the solar system taken by Voyager "
            "1. The spacecraft acquired a total of 60 frames for a "
            "mosaic of the solar system from a distance of more "
            "than 4 billion miles from Earth and about 32 degrees "
            "above the ecliptic. From Voyager's great distance "
            "Earth is a mere point of light, less than the size of "
            "a picture element even in the narrow-angle camera. "
            "Earth was a crescent only 0.12 pixel in size. "
            "Coincidentally, Earth lies right in the center of one "
            "of the scattered light rays resulting from taking the "
            "image so close to the sun. This blown-up image of the "
            "Earth was taken through three color filters - violet, "
            "blue and green - and recombined to produce the color "
            "image. The background features in the image are "
            "artifacts resulting from the magnification.",
            citation="NASA/JPL-Caltech",
            license="Public domain",
            size=0.4,
            tags=["pale blue dot", "voyager", "nasa", "jpl"],
            is_zip=True,
        )
