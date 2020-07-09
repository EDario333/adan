Funcion String <- get_file_name_without_extension(args)
	Si args == null Entonces
		Escribir "Tha args are missed!"
	FinSi
	
	return the_file_name_from_source_data_without_extension
//	For instance, if the source_data is something like:
//	file:///home/user/dir1/subdir1/subdir2/subdir_n/my_file.csv
//	the function will return the string my_file
//	For obvious reasons, this implementation will depend from the 
//	programming language
Fin Funcion

Funcion DataFrame <- read_csv_file(source_data)
	//	Leave the implementation to one library
	//	In Python could be Pandas or Numpy
Fin Funcion

Funcion DataFrame <- write_dataframe_to_csv_file(df, filename)
	//	Leave the implementation to one library
	//	In Python could be Pandas or Numpy
Fin Funcion

Funcion DataFrame <- concat_by_columns(df1, df2)
	//	Leave the implementation to one library
	//	In Python could be Pandas or Numpy
	// Must return df1 + df2, joined by columns
Fin Funcion

Funcion DataFrame <- take_a_sample(from_df, sample_size)
	//	Leave the implementation to one library
	//	In Python could be Pandas or Numpy
	// Of course that also we could write our implementation. 
	// I.e.: in a random way pick data (rows) from from_df
Fin Funcion

Funcion Serie <- pop_a_serie(from_df, serie_name)
	//	Leave the implementation to one library
	//	In Python could be Pandas or Numpy
	// return the serie popped. Note that from_df now doesn't 
	// contains the popped serie
FinFuncion

Funcion DataSet <- train_input_fn(features, labels, batch_size)
	//	Leave the implementation to one library
	//	In Python could be Tensorflow
FinFuncion

Funcion DataSet <- eval_input_fn(features, labels, batch_size)
	//	Leave the implementation to one library
	//	In Python could be Tensorflow
FinFuncion

Funcion DataFrame <- choose_random_features(args, source_df)
	Si args == null Entonces
		Escribir "Tha args are missed!"
	SiNo
		Si source_df == null Entonces
			Escribir "Please specify the source dataframe"
		FinSi
	FinSi
	
	tsfe = len(source_df.columns)
	ssfe = int(tsfe * args.spfe)
	
	series = []
	processed = []
	new_df = new DataFrame()
	
	x = RandInt(0, ssfe-1)
	
	Mientras len(new_df.columns) < ssfe Hacer
		Mientras x in proccessed Hacer
			x = RandInt(0, ssfe-1)
		FinMientras
		processed.insert(x)
		
		serie = source_df[source_df.columns[x]]
		new_df = concat_by_columns(new_df, serie)
		x = RandInt(0, ssfe-1)
	FinMientras
	
	filename = get_file_name_without_extension(args)
	filename += '-' + str(ssfe) + 'features-all-data.csv'
	write_dataframe_to_csv_file(new_df, filename)

	return new_df
Fin Funcion

Funcion DataFrame <- read_source_and_return_randomized_df(args)
	Si args == null Entonces
		Escribir "The args are missed!"
//		Quit()
	SiNO
		Si args.source_data == null Entonces
			Escribir "The source data is missed!"
//			Quit()
		FinSi
	FinSi

	df = read_csv_file(args.source_data)
	labels_serie = pop_a_serie(df, args.label)
	randomized_df = choose_random_features(args, df)
	randomized_df = concat_by_columns(randomized_df, labels_serie)
	return randomized_df
Fin Funcion

Funcion ADAN(data_source, label, hlan, npla)
	//	tsac = test_set_accuracy | Current test set accuracy
	tsac <- 0.00
	
	//	tsta = test_set_target_accuracy | The desired accuracy for the test set	
	tsta <- 0.95
	
	//	sptr = starting_percent_training | The percent of records/rows to consider for the training set
	sptr <- 0.75
	
	//	stpt = step_percent_training | How much will increment the sptr for each iteration
	stpt <- 0.01
	
	//	spfe = starting_percent_features | The percent of features/cols to consider	
	spfe <- 0.75
	
	//	stpf = step_percent_features | How much will increment the spfe for each iteration
	stpf <- 0.10
	
	//	sppr = starting_percent_prediction | The percent of records/rows to consider for the prediction set
	sppr <- 0.10	
	
	ts <- 1000
	
	ltst <- 1000

	initial_sptr <- sptr
	initial_ts <- ts
	
	LABELS = ['Class1', 'Class2', ..., 'Class_n']
	
	// Build the hidden layers with its units respectively
	hidden_units = []
	Para x<-0 Hasta hlan Hacer
		hidden_units.insert(npla[x])
	Fin Para

	Mientras tsac < tsta Hacer
		randomized_df = read_source_and_return_randomized_df(args)
		tsda <- len(randomized_df)

		// Calculate the sample size training:
		// sstr = total size data (tsda) * starting percent training (sptr)
		// this will return a float value, so we need to convert to int
		sstr = int(tsda * sptr)

		// Calculate the sample size features:
		// ssfe = total size features (tsfe) * starting percent features (spfe)
		// this will return a float value, so we need to convert to int
		ssfe = int(tsfe * spfe)

		df_training = take_a_sample(randomized_df, sstr)

		filename_ = get_file_name_without_extension(args)
		filename = filename_ + '-' + str(ssfe) + 'features-training-data-'
		filename += str(sstr) + '-rows.csv'
		write_dataframe_to_csv_file(df_training, filename)

		train_y = pop_a_serie(df_training, args.label)
		
		// The dataframe for testing will be all the records/rows
		// that exist in randomized_df but not in df_training
		// This is a difference, so highly probabadly will depend
		// from the programming language
		df_testing = randomized_df - df_training
		
		filename = filename_ + '-' + str(ssfe) + 'features-test-data-'
		filename += str(tsda-sstr) + '-rows.csv'
		write_dataframe_to_csv_file(df_testing, filename)
		
		test_y = pop_a_serie(df_test, args.label)

		n_rows_for_prediction = int(tsda * sppr)
		df_predict = take_a_sample(randomized_df, n_rows_for_prediction)
		file_name = file_name_ + '-' + str(ssfe) + 'features-predict-data-'
		file_name += str(n_rows_for_prediction) + '-rows.csv'
		write_dataframe_to_csv_file(df_predict, filename)
		
		predict_y = pop_a_serie(df_predict, args.label)
		expected_labels = []

		top = len(predict_y)

		Para x<-0 Hasta top Hacer
			expected_labels.insert(LABELS[predict_y[x]])
		Fin Para
		
		features = []
		
		top = len(df_training.columns)
		
		Para x<-0 Hasta top Hacer
			features.insert(df_training.columns[x].name)
		Fin Para

		classifier = new Classifier(features=features, hidden_units=hidden_units, n_classes=len(LABELS))
		classifier.train(input_function=train_input_fn(df_training, train_y, bs), steps=ts)

		results = classifier.evaluate(input_function=eval_input_fn(df_testing, test_y, bs))
		
		predictions = classifier.predict(input_function=eval_input_fn(df_predict, null, bs))
		
		Escribir predictions
		
		tsac = results.test_accuracy
		
		sptr = sptr + stpt
		
		Si sstr >= tsda Entonces
			sptr = initial_sptr
			ts = ts + 1
		FinSi

		Si ts > ltst Entonces
			sptr = initial_sptr
			ts = initial_ts
			spfe = spfe + stpf
		FinSi
	FinMientras
Fin Funcion