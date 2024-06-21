#!/usr/bin/env bash
#SBATCH --account=s2441
#SBATCH --time=59
#SBATCH --constraint=[cas|sky|mil]

PIXI=$HOME/.pixi/bin/pixi

$PIXI run python subset.py
