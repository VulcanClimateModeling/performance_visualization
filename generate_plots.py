import click
from typing import Optional
import os
import subprocess

from performance_plots.plotting import plotting
from summary_files.json_summary import analyze_foler as summarize_raw_files


def generate_timing_plots(file_directory):
    data_dir = file_directory + "/fv3core_performance/"
    plotting(data_dir)


def genererate_plain_text_profile_summary(file_directory):
    os.environ["experiment"] = "c128_6ranks_baroclinic"
    os.environ["backend"] = "gtc:gt:gpu"
    profile_path = file_directory + "/fv3core_profile/gtc_gt_gpu/prof"
    val = subprocess.check_call(
        "./performance_profile/plain_text_summary.sh '%s'" % profile_path,
        shell=True,
    )


def generate_plain_text_history(file_directory):
    os.environ["experiment"] = "c128_6ranks_baroclinic"
    history_path = file_directory + "/fv3core_performance/gtc_gt_gpu/"
    val = subprocess.check_call(
        "./summary_files/plain_text_summary.sh '%s'" % history_path,
        shell=True,
    )


def visualize_profile(file_directory):
    os.environ["experiment"] = "c128_6ranks_baroclinic"
    os.environ["backend"] = "gtc:gt:gpu"
    profile_path = file_directory + "/fv3core_profile/gtc_gt_gpu/prof"
    val = subprocess.check_call(
        "./performance_profile/visualize_profile.sh '%s'" % profile_path,
        shell=True,
    )


@click.command()
@click.argument("file_directory", required=True, nargs=1)
@click.argument("comparison_directory", required=False, default=None, nargs=1)
def driver(file_directory: str, comparison_directory: Optional[str]):
    if comparison_directory:
        print(
            "comparing data from "
            + comparison_directory
            + " with the lastest results in "
            + file_directory
        )
        raise NotImplementedError()
    else:
        print("generating visualization for performance data in " + file_directory)
        generate_timing_plots(file_directory)
        summarize_raw_files(file_directory)
        genererate_plain_text_profile_summary(file_directory)
        visualize_profile(file_directory)
        generate_plain_text_history(file_directory)


if __name__ == "__main__":
    driver()