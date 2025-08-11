# Skoltech_task

## Задача N1 - Имплементирование кода из статьи ROCKET(https://arxiv.org/abs/1910 13051)
Для задание был написан код: rocket.py - код для создания ядер, применения к рядам и получения набора признаков, для использования в классификаторе
Добавлены "kernels_model": normal, binary, ternary
Запуск программы осуществлялся через программу: main_algorithm.py

## Аргументы
```
- `-d, --dataset_names` : TXT-файл с названиями датасетов  
- `-i, --input_path`    : родительская директория с датасетами  
- `-o, --output_path`   : путь для сохранения результатов  
- `-n, --num_runs`      : число прогонов *(по умолчанию 10)*  
- `-k, --num_kernels`   : число ядер *(по умолчанию 10 000)*  
- `-m, --kernels_model`   : выбор модели *(по умолчанию normal)*
```

## Примеры запуска
```bash
> python main_algorithm.py -d ham.txt -i ./Ham -o ./ -n 10 -k 1000
> python main_algorithm.py -d ham.txt -i ./Ham -o ./ -n 10 -k 1000 -m binary
> python main_algorithm.py -d ham.txt -i ./Ham -o ./ -n 10 -k 1000 -m ternary
```

После запуска "main_algorithm.py" получены данные из Ham, был построен barplot для сравнения accuracy, и confedence interval (CI)

# Accuracy mean plot
<img width="1059" height="1842" alt="image" src="https://github.com/user-attachments/assets/60a47370-724c-4a19-96ea-1cd2877083d2" />

# Accuracy mean + errorbar
<img width="1630" height="909" alt="image" src="https://github.com/user-attachments/assets/40a299fd-eebf-415a-b0ac-7c56ff08098e" />

* [Rocket](task1_rocket/rocket.py)
* [Main Algorithm](task1_rocket/main_algorithm.py)
* [Results csv](task1_rocket/resample_results.csv)

Вывод: Для датасета Ham выбор типа ядра в ROCKET не оказывает сильного влияния на итоговую точность, модель даёт схожие результаты. Это может означать, что информативность признаков в данном случае слабо зависит от распределения весов в случайных ядрах, а сама архитектура ROCKET достаточно устойчива к их выбору. 

## Задача N2 - Написание модуля graph и применение для решения задачи выбора друзей
Для задания был написан модуль: graph.py, который умеет создавать графы, и работать с ними: создание, различные виды графа, отрисовка. Так же возможно создавать рандомный граф. В файле graph_test.ipynb можно посмотреть, как правильно использовать модуль.

* [Graph](task2_graph/Graph.py)
* [Examples](task2_graph/graph_test.py)

# Рандомный граф из 20 человек
<img width="739" height="656" alt="image" src="https://github.com/user-attachments/assets/8aaad531-fcc6-4b0d-be01-3b8a93d99edf" />
Количество и имена людей, кто идет на пикник: (4, ['Christopher Reese', 'Maria Diaz', 'Kyle Johnson', 'Raven Boyd'])

## Задача №3 - работа с Docker. Подсчет количества каждого слова и поиск топ 10 самых встречаемых

* [Count](task3_docker/word_count.sh)
* [Top10](task3_docker/top10_words.sh)
* [Dockerfile](task3_docker/Dockerfile)
* [Solve](task3_docker/output)

## Примеры запуска
```bash
> docker exec mycontainer /task3_docker/word_count.sh /task3_docker/dracula.txt /task3_docker/output
> docker exec mycontainer /task3_docker/top10_words.sh /task3_docker/output/word_count.txt /task3_docker/output
```
