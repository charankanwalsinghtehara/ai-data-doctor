from sklearn.model_selection import (
    train_test_split
)


def split_dataset(

    X,

    y,

    test_size=0.2,

    random_state=42
):
    """
    Split dataset into
    training and testing data.
    """

    return train_test_split(

        X,

        y,

        test_size=test_size,

        random_state=random_state
    )