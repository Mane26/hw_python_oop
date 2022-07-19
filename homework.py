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
    M_IN_KM: int = 1000
    training_type: str = ''

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
    run_1: int = 18
    run_2: int = 20
    in_hour: int = 60
    training_type: str = 'RUN'

    def get_spent_calories(self) -> float:
        return ((self.run_1 * self.get_mean_speed() -
                self.run_2) * self.weight /
                self.M_IN_KM * self.duration *
                self.in_hour)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    wlk_1: float = 0.035
    wlk_2: float = 2
    wlk_3: float = 0.029
    in_hour: int = 60
    training_type: str = 'WLK'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.wlk_1 * self.weight + (
                self.get_mean_speed() ** self.wlk_2 //
                self.height) * self.wlk_3 * self.height) *
                self.duration * self.in_hour)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    swm_1: float = 1.1
    swm_2: float = 2
    training_type: str = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return ((self.lenght_pool * self.count_pool) /
                self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.swm_1) *
                self.swm_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_dict[workout_type](*data)


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