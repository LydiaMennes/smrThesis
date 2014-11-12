/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package thesis_nn;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import org.neuroph.core.data.DataSet;
import org.neuroph.core.data.DataSetRow;

/**
 *
 * @author Lydia
 */
public class DataKeeper {
    
    private DataSet trainingSet;
    private DataSet validationSet;
    private DataSet testSet;
    
    private String additionalInfoTemp="";
    private ArrayList<String> additionalInfoTrain;
    private ArrayList<String> additionalInfoValidation;
    private ArrayList<String> additionalInfoTest;
    
    private Random rand;
    
    public DataKeeper(){
        rand = new Random();
        additionalInfoTrain = new ArrayList<String>();
        additionalInfoValidation = new ArrayList<String>();
        additionalInfoTest = new ArrayList<String>();
    }
    
    public void load_Data(String data_path, int num_inputs, int num_outputs, int total_nr_samples, int val_test_set_size, String division_path)
    {
        BufferedReader br = null;
        trainingSet = new DataSet(num_inputs, num_outputs);
        validationSet = new DataSet(num_inputs, num_outputs);
        testSet = new DataSet(num_inputs, num_outputs);
        ArrayList<String> division = new ArrayList<>(); 
        double prob_accept = (double)(val_test_set_size+20)/total_nr_samples;
        try {		
            br = new BufferedReader(new FileReader(data_path));
            String line;
            String cvsSplitByBig = ";";
            String cvsSplitBySmall = ",";
            int i = 0;
            while ((line = br.readLine()) != null) {
                // use comma as separator
                additionalInfoTemp = "";
                ArrayList<double[]> values = getValues(cvsSplitByBig, cvsSplitBySmall, line);
                if(i==0){
                    System.out.println("nr inputs " + values.get(0).length + " " + num_inputs);
                    System.out.println("nr outputs " + values.get(1).length + " " + num_outputs);
                    if(!additionalInfoTemp.equals("")){
                        System.out.println(additionalInfoTemp);
                    }
                    else{
                        System.out.println("no additional info");
                    }
                }
                double p = rand.nextDouble();
                
//                if( randInd <= testSetSize + 10 && testSet.size()<testSetSize)
                if( p<prob_accept && testSet.size()<val_test_set_size)
                {
                    testSet.addRow(new DataSetRow(values.get(0), values.get(1)));
                    if(!additionalInfoTemp.equals("")){
                        additionalInfoTest.add(additionalInfoTemp+","+Integer.toString(i));
                    }
                    division.add("test");
                }
                else if (p<2*prob_accept&& validationSet.size()<val_test_set_size)
                {
                    validationSet.addRow(new DataSetRow(values.get(0), values.get(1)));
                    if(!additionalInfoTemp.equals("")){
                            additionalInfoValidation.add(additionalInfoTemp+","+Integer.toString(i));
                        }
                    division.add("val");
                }
                else{           
//                    System.out.println(values.get(0).length+" "+ values.get(1).length);
                    trainingSet.addRow(new DataSetRow(values.get(0), values.get(1)));
                    if(!additionalInfoTemp.equals("")){
                            additionalInfoTrain.add(additionalInfoTemp+","+Integer.toString(i));
                        }
                    division.add("train");
                }
                if(i%500000==0){
                    System.out.println("Loaded sample " + i);
                }
                i++;
            } 
	} 
        catch (FileNotFoundException e) {e.printStackTrace();} 
        catch (IOException e) {e.printStackTrace();} 
        finally {
            if (br != null) {
                try {
                        br.close();
                } catch (IOException e) {e.printStackTrace();}
            }
	}
        save_division(division, division_path);
        System.out.println("Sizes train test val: "+trainingSet.size()+" "+testSet.size()+" "+validationSet.size());
    }
    
    public void load_data_with_division(String data_path, int num_inputs, int num_outputs, String division_path)
    {
        BufferedReader br = null;
        trainingSet = new DataSet(num_inputs, num_outputs);
        validationSet = new DataSet(num_inputs, num_outputs);
        testSet = new DataSet(num_inputs, num_outputs);        
        String div_elem = "";
        try {		
            br = new BufferedReader(new FileReader(data_path));
            BufferedReader br_div = new BufferedReader(new FileReader(division_path));
            String line;
            String cvsSplitByBig = ";";
            String cvsSplitBySmall = ",";
            int i = 0;
            while ((line = br.readLine()) != null) {
                // use comma as separator
                additionalInfoTemp = "";
                ArrayList<double[]> values = getValues(cvsSplitByBig, cvsSplitBySmall, line);
                if(i==0){
                    System.out.println("nr inputs " + values.get(0).length + " " + num_inputs);
                    System.out.println("nr outputs " + values.get(1).length + " " + num_outputs);
                    if(!additionalInfoTemp.equals("")){
                        System.out.println(additionalInfoTemp);
                    }
                    else{
                        System.out.println("no additional info");
                    }
                }
                div_elem = br_div.readLine();
                if( div_elem.equals("test"))
                {
                    testSet.addRow(new DataSetRow(values.get(0), values.get(1)));
                    if(!additionalInfoTemp.equals("")){
                        additionalInfoTest.add(additionalInfoTemp+","+Integer.toString(i));
                    }
                    
                }
                else if (div_elem.equals( "val"))
                {
                    validationSet.addRow(new DataSetRow(values.get(0), values.get(1)));
                    if(!additionalInfoTemp.equals("")){
                            additionalInfoValidation.add(additionalInfoTemp+","+Integer.toString(i));
                        }
                    
                }
                else if (div_elem.equals("train"))
                {           
//                    System.out.println(values.get(0).length+" "+ values.get(1).length);
                    trainingSet.addRow(new DataSetRow(values.get(0), values.get(1)));
                    if(!additionalInfoTemp.equals("")){
                            additionalInfoTrain.add(additionalInfoTemp+","+Integer.toString(i));
                        }
                    
                }
                else{
                    System.out.println("WRONG DIVISION ELEMENT");
                    System.out.println("-"+div_elem+"-");
                }
                if(i%500000==0){
                    System.out.println("Loaded sample " + i);
                }
                i++;
            } 
            br_div.close();
	}        
        catch (FileNotFoundException e) {e.printStackTrace();} 
        catch (IOException e) {e.printStackTrace();} 
        finally {
            if (br != null) {
                try {
                        br.close();
                } catch (IOException e) {e.printStackTrace();}
            }
	}
        System.out.println("Sizes train test val: "+trainingSet.size()+" "+testSet.size()+" "+validationSet.size());
    }
    
    private ArrayList<double[]> getValues(String cvsSplitByBig, String cvsSplitBySmall, String input) {
        ArrayList<double[]> values = new ArrayList<double[]>();
        String[] bigSplit = input.split(cvsSplitByBig);
        values.add(toDoubles(bigSplit[0], cvsSplitBySmall));
        values.add(toDoubles(bigSplit[1], cvsSplitBySmall));
        if(bigSplit.length>2){
            additionalInfoTemp = bigSplit[2];
        }
        return values;
    }
    
    private double[] toDoubles(String s, String splitBy) {
        String[] x = s.split(splitBy);
        double[] result =new double[x.length];
        for(int i = 0;i<x.length;i++)
        {
            result[i]= Double.parseDouble(x[i]);
        }
        return result;
    }

    public DataSet getTrainingSet() {
        return trainingSet;
    }

    public DataSet getValidationSet() {
        return validationSet;
    }

    public ArrayList<String> getAdditionalInfoTrain() {
        return additionalInfoTrain;
    }

    public ArrayList<String> getAdditionalInfoValidation() {
        return additionalInfoValidation;
    }

    public ArrayList<String> getAdditionalInfoTest() {
        return additionalInfoTest;
    }
    
    public String getAdditionalInfoTrainElem(int i) {
        return additionalInfoTrain.get(i);
    }

    public String getAdditionalInfoValidationElem(int i) {
        return additionalInfoValidation.get(i);
    }

    public String getAdditionalInfoTestElem(int i) {
        return additionalInfoTest.get(i);
    }

    public DataSet getTestSet() {
        return testSet;
    }
    
    public int[] getSizes(){
        int[] sizes = {trainingSet.size(), validationSet.size(),testSet.size()};
        return sizes;
    }
    
    public void printSizes(){
        System.out.print("trainingset ");
        System.out.println(trainingSet.size());
        System.out.print("validationset ");
        System.out.println(validationSet.size());
        System.out.print("testset ");
        System.out.println(testSet.size());
    }
    
    public void trimTrainingSetCategory(){
        double[] freqs = new double[trainingSet.getRowAt(0).getDesiredOutput().length];
        
        for(DataSetRow item: trainingSet.getRows()){
            double[] output = item.getDesiredOutput();
            for(int i =0;i<output.length;i++){
                if(output[i] == 1.0){
                   freqs[i]+=1.0;  
                   break;
                }
            }
        }
        
        double[] temp = freqs.clone();
        Arrays.sort(temp);
        double median = temp[(int)Math.round(temp.length/2.0)];
        
        double min = freqs[0];
        for(int i = 1; i<freqs.length;i++){
            if(freqs[i]<min){
                min = freqs[i];
            }
        }
        System.out.println("minimum= "+min);
        System.out.println("median= "+median);
        double[] reduce = new double[trainingSet.getRowAt(0).getDesiredOutput().length];
        for(int i = 0; i<freqs.length;i++){
            reduce[i] = Math.max((int)Math.round(freqs[i]-(median*1.3)),0);
            
        }
        reduceDataSet(trainingSet, freqs, reduce);        
    }

    private void reduceDataSet(DataSet dataSet, double[] freqs, double[] reduce) {
        double[] new_freqs = freqs.clone();
        for(int k = dataSet.size()-1;k>=0;k--){            
            double[] output = dataSet.getRowAt(k).getDesiredOutput();
            for(int i =0;i<output.length;i++){
                if(output[i] == 1.0){
                   if(rand.nextDouble()< reduce[i]/freqs[i]){
                       dataSet.removeRowAt(k);
                       new_freqs[i]--;
                   }
                   break;
                }
            }
        }
        System.out.println("old new");
        double sum_old = 0;
        double sum_new = 0;
        for(int i =0;i<freqs.length;i++){
            System.out.println(freqs[i]+" "+new_freqs[i]+" "+reduce[i]);
            sum_old+= freqs[i];
            sum_new+=new_freqs[i];
        }
        System.out.println("Sum");
        System.out.println(sum_old+" "+sum_new);
    }

    private void save_division(ArrayList<String> division, String division_path) {
       
        try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(division_path)))) {
            for(String s: division){
                out.write(s+"\n");
            }
        }catch (IOException e) {System.out.println("Exception in write to log smr networks");}
    }
}
