import pandas as pd
from typing import NamedTuple, Any, Callable, Iterable, Literal

from algos.factorized import AlgosComposer
from utils.timer import timer
from algos.factorized.dict_wrapper import AT
from pprint import pp
from tqdm import tqdm
import colorama
import sys


class TableRow(NamedTuple):
    sg_class: str
    args: Iterable[tuple[Any, ...]]

    time_mil: float
    time_cross: float

    table_lookups_mil: int
    table_lookups_cross: int

    checked_strings_mil: int
    checked_strings_cross: int

    replaced_old_strings_cross: int


def run_cmp(sg_class: Callable, args: tuple[Any, ...],
            log_to_std: bool = True, df: pd.DataFrame | None = None):
    # если надо, игнорируем вывод
    save_stdout = sys.stdout
    if not log_to_std:
        sys.stdout = open('/dev/null', 'w')

    # генерируем полугруппу
    x = sg_class(*args)
    print(x)

    # запускаем military алгоритм
    AT.reset()
    _, tm = timer(AlgosComposer.militaristic)(x)
    atm = AT.copy()
    pp(atm)

    # запускаем crossing алгоритм
    AT.reset()
    _, tc = timer(AlgosComposer.crossing_tree_like)(x, assert_check=False)
    atc = AT.copy()
    pp(atc)

    # вывод
    sec_diff = tc - tm
    times_diff = tc / tm
    succ, times_diff = (colorama.Fore.RED + 'SLOWER', times_diff) \
        if tc > tm \
        else (colorama.Fore.GREEN + 'FASTER', 1 / times_diff)
    print(f'\n>>🦤 diff {sec_diff}s')
    print(
        f'>>🦤 table lookups win {atm.table_lookups - atc.table_lookups}:  {100 - atc.table_lookups/atm.table_lookups*100:.2}%')
    print(f'>>🦤 {succ+colorama.Style.RESET_ALL} {times_diff:.2} times')

    # запись в таблицу
    if df is not None:
        row = TableRow(
            sg_class=sg_class.__name__, args=args,
            time_mil=tm, time_cross=tc,
            table_lookups_mil=atm.table_lookups, table_lookups_cross=atc.table_lookups,
            checked_strings_mil=atm.checked_real, checked_strings_cross=atc.checked_real,
            replaced_old_strings_cross=atc.replaced_old_strings
        )
        df.loc[len(df)] = tuple(row)  # type: ignore

    if not log_to_std:
        sys.stdout = save_stdout

    return tm + tc


class TestingSample(NamedTuple):
    func: Callable
    args: tuple[Any, ...]
    runs_number: int


def _run_single(ts: TestingSample, df: pd.DataFrame):
    for i, arg in enumerate(ts.args):
        for j in range(ts.runs_number):
            print(
                f'->> {ts.func.__name__:20} {str(i * ts.runs_number + j +1)+"/" + str(len(ts.args)*ts.runs_number):10} {str(arg):10}')
            run_cmp(ts.func, arg, log_to_std=False, df=df)


def run_many(tests: Iterable[TestingSample],
             df_path: str, csv_mode: Literal['w', 'a'] = 'a'):
    df = pd.DataFrame(columns=TableRow._fields)
    pp(tests)

    for ts in tests:
        _run_single(ts, df)

    df.to_csv(df_path, mode=csv_mode)
