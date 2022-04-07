import traceback


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


#  Задание 1
def match(string, pattern):
    #  Проверка допустимых символов в паттерне
    for i in pattern:
        if i not in ('a', '*', 'd', ' '):
            raise Exception('Паттерн с ошибками')

    #  Сравнение по строкам
    if len(string) == len(pattern):
        #  Проход посимвольно по паттерну и сравнение со string
        for index in range(len(pattern)):
            if pattern[index] == 'a':
                if not string[index].islower():
                    return False
            elif pattern[index] == 'd':
                if not string[index].isdigit():
                    return False
            elif pattern[index] == '*':
                if not (string[index].isdigit() or string[index].islower()):
                    return False
            elif pattern[index] == ' ':
                if not string[index] == ' ':
                    return False
        return True
    else:
        return False


def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ', 'a'))

    runner.expectTrue(lambda: match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda: match('x', 'w'))


tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов',
                         'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов',
                         'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}

tasks_list = []  # Массив всех задач группы
group_list = []  # Массив всех id групп


#  Поиск всех задач группы
def find_group_tasks(tasks, groupId):
    global tasks_list

    # Если дошли до полученного id
    if tasks['id'] == groupId:
        if tasks.get('priority') is None:  # Если это группа
            for child in tasks['children']: # Пробежка по детям группы
                find_group_tasks(child, child['id'])
        else:
            tasks_list.append(tasks)
    # Иначе проверяем детей проверенной группы
    elif tasks.get('priority') is None:
        for child in tasks['children']: # Пробежка по детям группы
            find_group_tasks(child, groupId)

#  Поиск всех id групп
def find_all_group(tasks):
    global group_list
    if tasks.get('priority') is None:  # Если это группа
        group_list.append(tasks['id'])
        for child in tasks['children']:  # Пробежка по детям группы
            find_all_group(child)


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
    global tasks_list
    global group_list
    tasks_list.clear()
    group_list.clear()
    find_group_tasks(tasks, groupId)
    find_all_group(tasks)

    #  Есть ли такая группа?
    if groupId in group_list:
        #  Пустая ли группа?
        if len(tasks_list) == 0:
            return None
        else:
            return sorted(tasks_list, key=lambda item: -item[
                'priority'])[0]
    #  Является ли задачей?
    elif tasks_list[0]['id'] == groupId:
        raise Exception('Является задачей')

    else:
        raise Exception('Группы не существует')


def taskEquals(a, b):
    return (
            not 'children' in a and
            not 'children' in b and
            a['id'] == b['id'] and
            a['name'] == b['name'] and
            a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(
        lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(
        lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
            'id': 8,
            'name': 'Выполнение тестов',
            'priority': 6,
        }))
    runner.expectTrue(
        lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
            'id': 3,
            'name': 'Подготовка релиза',
            'priority': 4,
        }))

    runner.expectTrue(
        lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)


testMatch()
testFindTaskHavingMaxPriorityInGroup()
