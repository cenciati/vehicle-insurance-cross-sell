from typing import Dict, List

import numpy as np


def mock_predict(size: int = 1) -> Dict[str, str | int] | List[Dict[str, str | int]]:
    """
    creates fake data to test the `predict` function.

    :param size: amount of data.
    :returns dict or a list of dicts with fake item(s).
    """
    assert size >= 1 and size != 0

    data = []
    if size > 1:
        while len(data) != size:
            data.append(mock_predict(size=1))

        assert len(data) == size

        return data

    return {
        "id": np.random.randint(1, 100),
        "Gender": np.random.choice(["Male", "Female"]),
        "Age": np.random.randint(10, 100),
        "Driving_License": np.random.randint(0, 2),
        "Region_Code": np.random.randint(1, 500),
        "Previously_Insured": np.random.randint(0, 2),
        "Vehicle_Age": np.random.choice(["< 1 Year", "1-2 Year", "> 2 Years"]),
        "Vehicle_Damage": np.random.choice(["Yes", "No"]),
        "Annual_Premium": np.random.randint(1, 100_000),
        "Policy_Sales_Channel": np.random.randint(1, 500),
        "Vintage": np.random.randint(1, 300),
    }
