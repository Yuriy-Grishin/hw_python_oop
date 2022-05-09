from dataclasses import dataclass, asdict
from typing import Dict, List, Any


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info: str = ('Тип тренировки: {training_type}; '
                 'Длительность: {duration:.3f} ч.; '
                 'Дистанция: {distance:.3f} км; '
                 'Ср. скорость: {speed:.3f} км/ч; '
                 'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод сообщения о тренировке."""
        return self.info.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_cal_run_1: float = 18
        coeff_cal_run_2: float = 20
        return ((coeff_cal_run_1 * self.get_mean_speed()
                - coeff_cal_run_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_cal_walk_1: float = 0.035
        coeff_cal_walk_2: float = 0.029
        coeff_cal_walk_3: float = 2
        return (coeff_cal_walk_1 * self.weight + (self.get_mean_speed()
                ** coeff_cal_walk_3 // self.height) * coeff_cal_walk_2
                * self.weight) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length: float = length_pool
        self.count: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.length * self.count / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        coeff_cal_swim_1: float = 1.1
        coeff_cal_swim_2: float = 2
        return ((self.get_mean_speed()
                + coeff_cal_swim_1) * coeff_cal_swim_2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Any] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_dict:
        raise KeyError(f'Неизвестный вид спорта:{workout_type}')
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())

    if __name__ == '__main__':
        packages = [
            ('SWM', [720, 1, 80, 25, 40]),
            ('RUN', [15000, 1, 75]),
            ('WLK', [9000, 1, 75, 180]),
        ]

        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)
