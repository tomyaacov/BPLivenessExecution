# BPLivenessExecution
Code appendix for the paper "Adding Liveness to Executable
Specifications"

<b>Note: the project was implemented and tested on Python 3.7.4</b>

## Installation
<ol>
<li>
Clone the project :

```shell
git clone https://github.com/bThink-BGU/BPLivenessExecution.git
```
</li>
<li>
Create a virtual environment and activate it:

```shell
cd BPLivenessExecution
python -m venv env 
source env/bin/activate
```
</li>
<li>
Update pip and install all dependencies:

```shell
pip install --upgrade pip
pip install -r requirements.txt
```
</li>
</ol>

## Usage
### running trained b-programs:
<ul>
<li>
Sokoban (for Sokoban maps 1-3):

```shell
python run_sokoban.py 1
```
</li>
<li>
Single Lane Bridge:

```shell
python lane_bridge_run_model.py
```
</li>
</ul>

### training b-programs:
<ul>
<li>
Sokoban (for Sokoban maps 1-3):

```shell
python train_sokoban.py 1
```
</li>
<li>
Single Lane Bridge:

```shell
python lane_bridge_experiment.py
```
</li>
</ul>
