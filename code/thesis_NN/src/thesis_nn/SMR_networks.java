/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package thesis_nn;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.neuroph.core.Layer;
import org.neuroph.core.NeuralNetwork;
import org.neuroph.core.Neuron;
import org.neuroph.core.data.DataSet;
import org.neuroph.core.data.DataSetRow;
import org.neuroph.core.transfer.TransferFunction;
import org.neuroph.nnet.MultiLayerPerceptron;
import org.neuroph.nnet.learning.MomentumBackpropagation;

/**
 *
 * @author lydia
 */
public class SMR_networks 
{        

    private static void weights_to_file(MultiLayerPerceptron m, String outputLocation, int i) {
        new File(outputLocation+"\\all_weights").mkdirs();
        String fileName = outputLocation+"\\all_weights\\weights_it"+Integer.toString(i)+".txt";
        try {
            FileWriter fileWriter = new FileWriter(fileName);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);                        
            Double[] weights = m.getWeights();
            for(int j =0;j<weights.length;j++){
                bufferedWriter.write(Double.toString(weights[j]));
                if(j!=weights.length-1){
                    bufferedWriter.write("\n");
                }
            }             
            bufferedWriter.close();
        }
        catch(IOException ex) {System.out.println("Error writing to file '"+ fileName + "'");}

    }

    private static void write_to_log(String outputLocation, int iter, String date, double error, double acc, double acc_train, double acc_test) {
        String filename = outputLocation+"\\log.txt";
        try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(filename, true)))) {
            out.print("It ,"+Integer.toString(iter)+", err, "+Double.toString(error)+ ", acc val, "+Double.toString(acc)+", acc train, "+Double.toString(acc_train)+", acc test, "+Double.toString(acc_test)+"\n");
        }catch (IOException e) {System.out.println("Exception in write to log smr networks");}
    }

    private Random rand;
    DateFormat dateFormat = new SimpleDateFormat("dd/MM HH:mm:ss");   

    //For simple neural net
    private MultiLayerPerceptron simpleNeuralNet;
    private MultiLayerPerceptron complexNeuralNet;
    private MomentumBackpropagation mbp;

    private int num_inputs;
    private int num_hidden;
    private int num_outputs;

    DataKeeper data;
    
    
    
    public SMR_networks(int num_input, int num_hidden, int num_output)
    {
            //System.out.println("Initializing neural network with " + num_inputs + " inputs, " + num_hidden + " hidden nodes and 1 output.");
            this.rand = new Random();
            this.num_inputs = num_input;
            this.num_hidden = num_hidden;
            this.num_outputs = num_output;
            buildNetwork_simple();
    }
    
    public SMR_networks(int num_input, int num_hidden, int num_output, int[] patchsizes)
    {
            //System.out.println("Initializing neural network with " + num_inputs + " inputs, " + num_hidden + " hidden nodes and 1 output.");
            this.rand = new Random();
            this.num_inputs = num_input;
            this.num_hidden = num_hidden;
            this.num_outputs = num_output;
            buildNetwork_complex(patchsizes);
    }
    
    public SMR_networks(String neural_net_file, String type)
    {
            //System.out.println("Initializing neural network with " + num_inputs + " inputs, " + num_hidden + " hidden nodes and 1 output.");
            this.rand = new Random();
            if(type.equals("simple"))
            {
                simpleNeuralNet = loadNetwork(neural_net_file);
            }            
    }
    
    private void buildNetwork_complex(int[]patchSizes)                    
    {
            System.out.println("Not implemented yet");
            // build network with three layers
            // Remove connections using the removeInputConnection method from the class Neuron

    }
    
    
    public void addLearningRule_errorTrainSet(MultiLayerPerceptron m, double min_error, double learning_rate, double momentum_rate, int max_iterations)
    {
        mbp = new MomentumBackpropagation();        
        mbp.setMaxError(min_error);
        mbp.setLearningRate(learning_rate);
        mbp.setMomentum(momentum_rate);
        mbp.setMaxIterations(max_iterations);

        m.setLearningRule(mbp);
        System.out.println("Network created");
    }
    
     public void addLearningRule_errorValSet(MultiLayerPerceptron m, double learning_rate, double momentum_rate)
    {
        mbp = new MomentumBackpropagation(); 
        mbp.setLearningRate(learning_rate);
        mbp.setMomentum(momentum_rate);
        mbp.setMaxIterations(200);
        m.setLearningRule(mbp);
        System.out.println("Network created");
    }
    
    
    private void buildNetwork_simple() 
    {
        System.out.println("Create network");
        simpleNeuralNet = new MultiLayerPerceptron(num_inputs, num_hidden, num_outputs);
        
        System.out.print(num_inputs+" ");
        System.out.print(num_hidden+ " ");
        System.out.println(num_outputs);
        for(int i = 0;i<simpleNeuralNet.getLayersCount();i++)
        {
            System.out.println(simpleNeuralNet.getLayerAt(i).getNeuronsCount());
        }
        
        
        for (int i = 0; i < num_hidden; i++)
        {
                simpleNeuralNet.getLayerAt(1).getNeuronAt(i).setTransferFunction(new Sigmoid(1));
        }
        for (int i = 0; i < num_outputs; i++)
        {
                simpleNeuralNet.getLayerAt(2).getNeuronAt(i).setTransferFunction(new Sigmoid(1));
        }

        
    }
    
    public void addData(DataKeeper d){
        data = d;
    }   

    static double[] getError(MultiLayerPerceptron simpleNeuralNet, DataSet dataset) 
    {
        double[] output;
        double sse = 0.0;
        for(int i = 0;i<dataset.size();i++)
        {
            output = predictLabel(dataset.getRowAt(i).getInput(), simpleNeuralNet);
            double[] label = dataset.getRowAt(i).getDesiredOutput();
            for(int j=0; j<label.length;j++)
            {
                sse += Math.pow(label[j]-output[j], 2);
            }
        }
        double msse_sample = sse/dataset.size();
        double msse_word = msse_sample/simpleNeuralNet.getOutputsCount();
        double[] result = {sse, msse_sample, msse_word};
        return result;
    }

    @SuppressWarnings("SleepWhileInLoop")
    private void train_old(MultiLayerPerceptron neuralNet, DataSet trainingSet) {
        neuralNet.learnInNewThread(trainingSet);
        boolean continueTraining = true;
        double error;
        int iteration;
        int minutes = 0;
        while(continueTraining){
            //every 5 minutes
            try{
                Thread.sleep(300000);
            }
            catch (InterruptedException e){}
            minutes+=5;
            error = neuralNet.getLearningRule().getPreviousEpochError();
            iteration = neuralNet.getLearningRule().getCurrentIteration();
            continueTraining = error >= neuralNet.getLearningRule().getMaxError() && iteration>1;
//            System.out.print(neuralNet.getLearningThread().getState());
            System.out.print(" Iteration ");
            System.out.print(iteration);
            System.out.print(" Error on trainingset ");
            System.out.print(error);
            double errorValSet = getError(simpleNeuralNet, data.getValidationSet())[2];
            System.out.print(" error on validation set ");
            System.out.print(errorValSet);
            System.out.print(" at minute");
            System.out.print(minutes);
            Date date = new Date();
            System.out.print(" at ");
            System.out.println(dateFormat.format(date));
        }
        neuralNet.stopLearning();
        System.out.println("Learning ended");        
        
    }
        
    public void train(MultiLayerPerceptron neuralNet, int nr_stable_its, double max_change_val, String log_location) throws IOException {
              
        System.out.println("Start training");
        boolean continueTraining = true;
        double[] errorsTrainSet;
        double[] errorsValSet;
        int iteration;
        int currentIteration = 0;
        int nrIterationsStable = 0;
        double lastErrorValSet = 0.0;
        BufferedWriter bf = new BufferedWriter ( new FileWriter(log_location+"\\log.txt"));
        bf.close();
        this.simpleNeuralNet=neuralNet;
        neuralNet.learnInNewThread(data.getTrainingSet());
        if(!neuralNet.getLearningThread().isAlive()){
                System.out.println("Thread has died immdediately");
        }
        while(continueTraining){
            if(!neuralNet.getLearningThread().isAlive()){
                System.out.print("Thread has died blaat");
            }
            try{
                Thread.sleep(1000);
                System.out.print(".");
            }
            catch (InterruptedException e){}
            if(!neuralNet.getLearningThread().isAlive()){
                System.out.println("Thread has died");
            }
            iteration = neuralNet.getLearningRule().getCurrentIteration();
            System.out.print(iteration);
            if (iteration>currentIteration){
                currentIteration = iteration;
                errorsTrainSet = getError(neuralNet, data.getTrainingSet());
                errorsValSet = getError(neuralNet, data.getValidationSet());
                if(Math.abs(errorsValSet[2]-lastErrorValSet)<max_change_val){
                    nrIterationsStable++;
                }
                else{
                    nrIterationsStable=0;
                }
                continueTraining = !(nrIterationsStable==nr_stable_its) && neuralNet.getLearningThread().isAlive();
                
                addToLog(log_location, iteration, errorsTrainSet[2], errorsValSet[2], nrIterationsStable, lastErrorValSet);
                if(iteration%1==0){
                    System.out.println("");
                    printStatus(iteration, errorsTrainSet[2], errorsValSet[2], nrIterationsStable, lastErrorValSet);                    
                    saveNetwork(neuralNet, log_location+"\\temp_NN_"+Integer.toString(iteration)+".nnet", "simple");
                }
                lastErrorValSet=errorsValSet[2];
            }
        }
        
        neuralNet.stopLearning();
        System.out.println("Learning ended"); 
    }    
    
    private void printStatus(int iteration, double errorTrainSet, double errorValSet, int nrIterationsStable, double lastErrorValSet) {
        System.out.print(" Iteration ");
        System.out.print(iteration);
        System.out.print(" Err on trainset ");
        System.out.print(errorTrainSet);
        System.out.print(" Err on valset ");
        System.out.print(errorValSet);
        System.out.print(" dif err valset ");
        System.out.print(errorValSet-lastErrorValSet);
        System.out.print(" stabel its ");
        System.out.print(nrIterationsStable);
        Date date = new Date();
        System.out.print(" at ");
        System.out.println(dateFormat.format(date));
    }

    private void addToLog(String log_location, int iteration, double errorTrainSet, double errorValSet, int nrIterationsStable, double lastErrorValSet)  {
        BufferedWriter w;
        try {
            w =   new BufferedWriter ( new FileWriter(log_location+"\\log.txt", true));
            w.write("Iteration "+Integer.toString(iteration));
            w.write(" Err on trainset "+Double.toString(errorTrainSet));
            w.write(" Err on valset "+Double.toString(errorValSet));
            w.write(" dif err valset "+Double.toString(errorValSet-lastErrorValSet));
            w.write(" stabel its "+Integer.toString(nrIterationsStable));
            Date date = new Date();
            w.write(" at "+dateFormat.format(date)+"\n");
            w.close();
        } catch (IOException ex) {
            Logger.getLogger(SMR_networks.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }

    

    
    
    private class Sigmoid extends TransferFunction
    {
            private static final long serialVersionUID = 1L;

            private final double factor;

            public Sigmoid(double factor)
            {
                    this.factor = factor;
            }

            @Override
            public double getOutput(double net)
            {
                    double o = factor * (net / (3 * Math.sqrt(1 + Math.pow(net / 3, 2))));

                    if (Double.isNaN(o))
                    {
                            if (net == Double.POSITIVE_INFINITY || net > 0)
                            {
                                    return 1;
                            }
                            else
                            {
                                    return -1;
                            }
                    }
                    //System.out.println("Output: " + o);
                    return o;
            }

            @Override
            public double getDerivative(double net)
            {
                    double d = (9 * factor) / (Math.pow(9 + Math.pow(net, 2), 3.0 / 2.0));

                    if (Double.isNaN(d))
                    {
                            return 0;
                    }
                    //System.out.println("Derivative: " + d);
                    return d;
            }
    }
    
    static double[] predictLabel(double[] values, MultiLayerPerceptron x)
    {
        x.setInput(values);
        x.calculate();
        return x.getOutput();
    }
    
    public void saveSimpleNetwork(String fileName){
        saveNetwork(simpleNeuralNet, fileName, "simple");
    }
    
    public MultiLayerPerceptron getSimpleNetwork()
    {
        return simpleNeuralNet;
    }
    
    public MultiLayerPerceptron getComplexNetwork()
    {
        return complexNeuralNet;
    }
    
    static void saveNetwork(MultiLayerPerceptron m, String fileName, String networktype)
    {

        try {
            FileWriter fileWriter = new FileWriter(fileName);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
            
            bufferedWriter.write(networktype);
            bufferedWriter.newLine();
            bufferedWriter.write(Integer.toString(m.getLayerAt(0).getNeuronsCount()-1)+" ");
            bufferedWriter.write(Integer.toString(m.getLayerAt(1).getNeuronsCount()-1)+" ");
            bufferedWriter.write(Integer.toString(m.getLayerAt(2).getNeuronsCount()));                
            bufferedWriter.newLine();
            Double[] weights = m.getWeights();
            for(int i =0;i<weights.length;i++){
                bufferedWriter.write(Double.toString(weights[i]));
                if(i!=weights.length-1){
                    bufferedWriter.write(" ");
                }
            }             
            bufferedWriter.close();
        }
        catch(IOException ex) {System.out.println("Error writing to file '"+ fileName + "'");}

    }
    
    static MultiLayerPerceptron loadNetwork(String fileName)
    {
        System.out.println("\nLOAD NETWORK");
        // This will reference one line at a time
        String line;
        int linenr = 0;
        ArrayList<Integer> layerSizes = new ArrayList<Integer>();
        ArrayList<Double> weights = new ArrayList<Double>();
        String type="";
        
        try {
            // FileReader reads text files in the default encoding.
            FileReader fileReader = new FileReader(fileName);
            // Always wrap FileReader in BufferedReader.
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            while((line = bufferedReader.readLine()) != null) {
                //PROCESS
                String[] elems = line.split(" ");
                if(linenr==0){
                    if(!elems[0].equals("simple") && !elems[0].equals("complex")){
                        System.out.println("Wrong network type encountered");
                    }
                    else {
                        type = elems[0];
                    }             
                }
                else if(linenr==1){
                    for(String e: elems){
                        layerSizes.add(Integer.parseInt(e));
                    }
                }
                else if(linenr==2)
                {
                    for(String e: elems){
                        weights.add(Double.parseDouble(e));
                    }
                }
                linenr++;
            }	
            // Always close files.
            bufferedReader.close();			
        }
        catch(FileNotFoundException ex){System.out.println("Unable to open file '" + fileName + "'");}
        catch(IOException ex) {System.out.println("Error reading file '"+ fileName + "'");}
        MultiLayerPerceptron m =  new MultiLayerPerceptron(layerSizes.get(0), layerSizes.get(1), layerSizes.get(2));
        if(type.equals("complex")){
            layerSizes.remove(0);
            layerSizes.remove(0);
            layerSizes.remove(0);
            removeConnections(m, layerSizes);
        }
        double[] weightsArray = new double[weights.size()];
        for(int i=0;i<weights.size();i++){
            weightsArray[i]=weights.get(i);
        }
        
        m.setWeights(weightsArray);
        System.out.println("Network loaded");
        return m;
    }
    
    static double[] activationOfLayer(MultiLayerPerceptron m, double[] sample, int layer)
    {
        double[] activation = new double[m.getLayerAt(layer).getNeuronsCount()]; 
        m.setInput(sample);
        m.calculate();
        for(int i =0;i<activation.length;i++)
        {
            Neuron n = m.getLayerAt(layer).getNeuronAt(i);
            activation[i]= n.getTransferFunction().getOutput(n.getNetInput());
        }
        return activation;
    }
    
    private static void removeConnections(MultiLayerPerceptron m, ArrayList<Integer> patchSizes) {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
    
    public static void superSimple(DataKeeper data,String outputLocation, int nr_inputs, int nr_outputs, int nr_hidden, int max_it, double alpha, double momentum){
        DataSet s = data.getTrainingSet();
        System.out.println("Init network");
        MultiLayerPerceptron m = new MultiLayerPerceptron(nr_inputs, nr_hidden, nr_outputs);
        MomentumBackpropagation mbp_simple = new MomentumBackpropagation();
        mbp_simple.setMaxIterations(max_it);
        mbp_simple.setLearningRate(alpha);
        mbp_simple.setMomentum(momentum);
        m.setLearningRule(mbp_simple);
        m.learnInNewThread(s);
        
        DateFormat df = new SimpleDateFormat("dd/MM HH:mm:ss");
        boolean continue_loop = true;
        int current_it = 0;
        System.out.println("start learning");
        double best_acc = 0;
        double acc;
        double acc_train;
        double acc_test;
        
        String filename = outputLocation+"\\log.txt";
        try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(filename)))) {}catch (IOException e) {System.out.println("Exception in creating log file");}
        
        while(continue_loop){
            int i = m.getLearningRule().getCurrentIteration();
//            System.out.println("iter"+i);
            if( current_it < i){
//                System.out.println("iter="+i);
                current_it = i;
                m.getLearningRule().pause();                
                acc = get_accuracy_classes(data.getValidationSet(), m);
                acc_train = get_accuracy_classes(data.getTrainingSet(), m);
                acc_test = get_accuracy_classes(data.getTestSet(), m);
                if(acc > best_acc){
                    saveNetwork(m, outputLocation+"\\best_network.nn", "simple");
                }
                weights_to_file(m, outputLocation, current_it);
                m.getLearningRule().resume();
                Date date = new Date();                
//                if(i<10 || i%10==0){
                if(i==1 || (i%10==0 && i > 0)){
//                if(i%10==0){
                    System.out.print(df.format(date)+" ");
                    System.out.format("it: %03d", i);                
                    System.out.format(" error: %.5f",m.getLearningRule().getPreviousEpochError());                
                    System.out.format(" acc val: %.5f acc train %.5f acc test %.5f\n", acc, acc_train, acc_test);
                }
                write_to_log(outputLocation, i, df.format(date), m.getLearningRule().getPreviousEpochError(), acc, acc_train, acc_test);
            }
            continue_loop = i < mbp_simple.getMaxIterations();
        }
        
        System.out.println("To file\n");
        String[] filenames = {outputLocation+"\\validationset.csv", outputLocation+"\\testset.csv"};
        
        ArrayList<String> additionalInfo = data.getAdditionalInfoValidation();
        List<DataSetRow> data_set = data.getValidationSet().getRows();
        List<DataSetRow> test_set = data.getTestSet().getRows();
              
        MultiLayerPerceptron best = loadNetwork(outputLocation+"\\best_network.nn");
        for(int i = 0; i<2;i++)
        {
            String output_string;
            if(i == 1){
                data_set =  test_set;
                additionalInfo =  data.getAdditionalInfoTest();
            }
            int itemnr = 0;
            
            
            try (FileWriter file = new FileWriter(filenames[i])) {
                for(DataSetRow item: data_set){
                    output_string = "";
                    String sep = ",";
                    output_string+=Double.toString(item.getInput()[4])+sep;


                    best.reset();
                    best.setInput(item.getInput());
                    best.calculate();
                    double[] output = best.getOutput(); 

                    int max_ind = 0;
                    for(int j = 1; j<output.length;j++){
                        if(output[j]>output[max_ind])
                            max_ind = j;
                    }
                    output_string+=Integer.toString(max_ind)+sep; 

                    String info = additionalInfo.get(itemnr);                
                    output_string+=info+"\n";
                    
                    file.write(output_string);

                    if(itemnr<5){
                        System.out.print(output_string);
                    }     
                    if(itemnr%10000==0)
                    {
                        System.out.println("itemnr"+Integer.toString(itemnr));
                    }
                    itemnr++;
                }
                file.close();
            } catch (IOException ex) {Logger.getLogger(SMR_networks.class.getName()).log(Level.SEVERE, null, ex);}         
            
            
            
        }        
                
    }
    
    public static double get_accuracy_classes(DataSet ds, MultiLayerPerceptron nw){
        int nr_correct = 0;
        for(DataSetRow sample : ds.getRows()){
            nw.reset();
            nw.setInput(sample.getInput());
            nw.calculate();
            double[] nw_output = nw.getOutput();
            int max_ind = 0;
            for(int i =1; i<nw_output.length;i++){
                if(nw_output[i]>nw_output[max_ind])
                    max_ind=i;
            }            
            if(sample.getDesiredOutput()[max_ind] == 1.0)
                nr_correct++;
        }
//        System.out.format("correct and size %d, %d\n", nr_correct, ds.size());
        return (double)nr_correct/ ds.size();
    }
    
}
