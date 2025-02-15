Create conda environment from scratch
`conda create -n riddler python=3.11 numpy matplotlib scipy`
`conda env export --from-history > environment.yml`

Create conda environment from YAML file
`conda create -f environment.yml`

