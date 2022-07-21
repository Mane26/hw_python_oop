class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories


    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср.скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}. ')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOURS: float = 60

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLICATOR: float = 18
    RUNNING_COEFF: float = 20

    def get_spent_calories(self)-> float:
        """"Получить количество затраченных калорий для бега."""
        return ((self.SPEED_MULTIPLICATOR * self.get_mean_speed()
                - self.RUNNING_COEFF) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOURS)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_FOR_WEIGHT: float = 0.035
    COEFF_FOR_HEIGHT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        pass

    def get_spent_calories(self)-> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        return ((self.COEFF_FOR_WEIGHT * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_FOR_HEIGHT * self.weight)
                * self.duration * self.MIN_IN_HOURS)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_ACTIVITY: float = 1.1
    SWIMMING_STYLE: float = 2
    training_type: str = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # длина_бассейна * count_pool
        # / M_IN_KM / время_тренировки
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self)-> float:
        """Получить количество затраченных калорий."""
        # (средняя_скорость + 1.1) * 2 * вес
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_dict:
        return training_dict[workout_type](*data)
    else:
        raise TypeError(f'Тренировка с кодом {workout_type} не распознана')


def main(training: Training) -> None:
    """Главная функция."""
    if training is not None:
        info = training.show_training_info()
        message_info = info.get_message()
        print(message_info)
    else:
        print('Error')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)