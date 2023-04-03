class InfoMessage:
    """Информационное сообщение о тренировке."""
    message = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self):
        return self.message.format(self.training_type, self.duration,
                                   self.distance, self.speed, self.calories)


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration
                * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_COEFFICIENT: float = 0.035
    CALORIES_MEAN_SPEED: float = 0.278
    LENGTH_MEANS_METER: int = 100
    CALORIES_COEFFICIENT_SHIFT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_COEFFICIENT
                * self.weight
                + ((self.get_mean_speed()
                    * self.CALORIES_MEAN_SPEED)**2
                    / (self.height
                 / self.LENGTH_MEANS_METER))
                * self.CALORIES_COEFFICIENT_SHIFT
                * self.weight)
                * (self.duration
                * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SHIFT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MEAN_SHIFT
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters: dict[str, type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in parameters:
        return parameters[workout_type](*data)
    raise ValueError("Тренировка не найдена")


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
