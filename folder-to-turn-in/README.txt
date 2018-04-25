Welcome to the README file for the Strattonn trading system.
This file will tell you about the organization of the Stratton directory, how
to use the software, and what required packages need installing.

==== Organization ====
	All Python files needed for using this system are kept at the top level
of the directory. The main file that needs to be run to use the system
is Strattonn.py.

	To run a genetic search, look at the examples in GNN_stock-VTI-5hl.py.
This file shows how to run a genetic search with the stock symbol VTI.

	Downloaded and formatted data is kept in the directory 'data'. Each
subdirectory corresponds to a different time interval. All data with a
1 minute time interval is kept in '1min' folder, all data with a daily
time interval is kept in the 'daily' time interval folder.

	Functions used to update and append data are in AlphaVantage.py.
	Functions used to calculate data statistics are in PreprocessCsv.py
and framePrepDnn.py.
	Functions used to perpare data for training and testing in a neural
network are in LoadData.py.
	The DNN class, responsible for creating deep neural networks, is in
DNN.py. Its data access object is in DNN_dao.py.
	The Chromosome class, responsible for representing neural network
architectures, is in Chromosome.py. Its data access object is in
Chromosome_dao.py.
	The Genetic Search algorithm class is in GeneticSearchDNN.py.
	Paths.py contains functions for creating data file paths based on
differences in operating system and stock symbol / time series.
	The text interface for the Strattonn system is in Strattonn.py.

==== Required Packages ====
	The Python runtime is required to run Strattonn.py with at least version
3.5. The pip package manager is recommended to install the Python libraries
needed.

	Required libraries:

tensorflow
keras
* all the dependencies of these libraries are required, but pip should
	handle that

==== Running ====
	To use the main Strattonn system, run the file Strattonn.py with the
Python3 interpreter. You will be presented with a menu of options. They
are described below. Type the number of the option you want and hit
'Enter'.

(1) Update Symbol Data
	Download the most recent data for a particular stock symbol and append
it to existing data. You will be asked for the following parameters:

stock symbol: Stock symbol for a company for fund (Ex. AAPL, VTI)
time series: Space in between data points. A daily time series will have stock
	price statistics for each day. Valid time series are TIME_SERIES_MONTHLY,
	TIME_SERIES_WEEKLY, TIME_SERIES_DAILY, TIME_SERIES_INTRADAY.
time interval: Leave this blank for time series other than TIME_SERIES_INTRADAY.
	This is the subdivision of the intraday time series. Valid options for this
	are 1min, 5min, 15min, 30min, 60min.

(2) Load Model
	Load a saved neural network model as the current model being used. Enter the
relative path to the model's save directory from the Strattonn file. Full file paths
work as well.

(3) Save Model
	Save the current neural network model to permanent storage. Enter the relative
or full path to the directory where you want to save the model.

(4) Train New/Current Model
	Train a neural network on data of your choice. If no model has been trained
or loaded, an untrained model will be created. Neural network architectures are 
chosen based on combination of stock symbol, time series, and time interval chosen.
You will be asked for the following parameters:

stock symbol: Stock symbol for a company for fund (Ex. AAPL, VTI)
time series: Space in between data points. A daily time series will have stock
	price statistics for each day. Valid time series are TIME_SERIES_MONTHLY,
	TIME_SERIES_WEEKLY, TIME_SERIES_DAILY, TIME_SERIES_INTRADAY.
time interval: Leave this blank for time series other than TIME_SERIES_INTRADAY.
	This is the subdivision of the intraday time series. Valid options for this
	are 1min, 5min, 15min, 30min, 60min.
fraction of data to test with: The fraction of data for that symbol and time
	series to use for testing, not training. The testing data is always the last
	portion of the data and is kept in chronological order. Training data is
	randomized. This should be a number between 0 and 1. Any choice less than
	0.05 will be changed to 0.05 and any choice greater than 0.95 will be made
	0.95.
epochs to train network for: The number of times the neural network trainer
	will feed the whole series of input data into the network and train it.
batch size: The number of batches the neural network trainer will split the
	data into. Each batch will be run through the network before back propogation
	training occurs.

	The system will train a neural network with the parameters you supply and
evaluate it. The number it prints out at the end is directional accuracy.
Directional accuracy is a metric of how well the network performs. It is the
fraction of times the neural network accurately predicted a price rise or fall
from one time step to the next on the testing data. A directional accuracy of 1
is perfect, while 0.5 is no better than chance.

	The trained model will be saved in memory as the current working model.

(5) Trade with Current Model
	Evaluate the current model's directional accuracy on a dataset of your
choice. Ideally, this option would run a simulated trading bot on that dataset.
We did not get this implemented, sadly :(

	You will be asked for the following parameters. When choosing the fraction
of testing data, only the testing portion of the dataset will be used for
evaluation.

stock symbol: Stock symbol for a company for fund (Ex. AAPL, VTI)
time series: Space in between data points. A daily time series will have stock
	price statistics for each day. Valid time series are TIME_SERIES_MONTHLY,
	TIME_SERIES_WEEKLY, TIME_SERIES_DAILY, TIME_SERIES_INTRADAY.
time interval: Leave this blank for time series other than TIME_SERIES_INTRADAY.
	This is the subdivision of the intraday time series. Valid options for this
	are 1min, 5min, 15min, 30min, 60min.
fraction of data to test with: The fraction of data for that symbol and time
	series to use for testing, not training. The testing data is always the last
	portion of the data and is kept in chronological order. Training data is
	randomized. This should be a number between 0 and 1. Any choice less than
	0.05 will be changed to 0.05 and any choice greater than 0.95 will be made
	0.95.

(6) Clear Current Model
	Delete the current working model from memory. A new untrained model will
be created when you train again.

(0) Quit
	Never use this option. It quits the Strattonn trading system. Why would
you want to do that?
