from dataclasses import dataclass, asdict
from typing import Union, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает информацию о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Инициализация свойств."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в {type(self).__name__}.'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных калорий."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MINUTES_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFFICIENT_WEIGHT_1 = 0.035
    COEFFICIENT_WEIGHT_2 = 0.029
    METER_PER_SECOND_COEFFICIENT = round(Training.M_IN_KM / 3600, 3)
    SPEED_DEGREE_INDICATOR = 2
    CM_IN_M = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        """Инициализация свойств."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных калорий."""
        return (
            (
                self.COEFFICIENT_WEIGHT_1
                * self.weight
                + (
                    (
                        self.get_mean_speed()
                        * self.METER_PER_SECOND_COEFFICIENT
                    )
                    ** self.SPEED_DEGREE_INDICATOR
                    / (
                        self.height
                        / self.CM_IN_M
                    )
                )
                * self.COEFFICIENT_WEIGHT_2
                * self.weight
            )
            * self.duration
            * self.MINUTES_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int
    ) -> None:
        """Инициализация свойств."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость во время тренировки в км/ч."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных калорий."""
        return (
            (
                self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )


TRAINING_TYPES: dict[str, Type[Union[Running, Swimming, SportsWalking]]] = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}


def read_package(training_type: str, training_data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if training_type not in TRAINING_TYPES:
        raise KeyError(f'Unknown training type: {training_type}')
    return TRAINING_TYPES[training_type](*training_data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, workout_data in packages:
        workout = read_package(workout_type, workout_data)
        main(workout)
