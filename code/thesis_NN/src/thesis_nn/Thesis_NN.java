/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package thesis_nn;


import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.logging.Level;
import java.util.logging.Logger;
//import org.neuroph.core.NeuralNetwork;
//import org.neuroph.core.data.DataSet;
//import org.neuroph.core.data.DataSetRow;
//import org.neuroph.nnet.Perceptron;


/**
 *
 * @author lydia
 */
public class Thesis_NN {
    
       
    public static void experiment_classes_optimize(String case_name, int window_size, int nr_inputs, String sub_folder, String run_suffix){
        DataKeeper d = new DataKeeper();
        
        int n = 1295875-(2*100000);
        int n_other = 100000;        
        System.out.println("n="+n+" size test ="+ n_other);
        int max_it = 100;        
        String data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        
        int nr_categories = 6;
        
        System.out.println("LOAD DATA");
        String division_file = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+sub_folder+"\\div_classes_optimize.txt";
        d.load_Data(data, nr_inputs, nr_categories, n-(2*n_other), n_other, division_file);
        
        System.out.println("START experiment "+run_suffix);        
//        setting = nr_inputs, window_size, nr_hidden, alpha, momentum
        ArrayList<double[]> settings = new ArrayList();
        settings.add(new double[]{60, 0.005, 0.05});
        settings.add(new double[]{60, 0.0005, 0.005});
        settings.add(new double[]{80, 0.005, 0.05});
        settings.add(new double[]{80, 0.0005, 0.005});
                
        int hidden;
        double alpha;
        double momentum;
        for(int i =0; i<settings.size();i++){
            System.out.println("Experiment "+i);
            hidden = (int)settings.get(i)[0];
            alpha = settings.get(i)[1];
            momentum = settings.get(i)[2];
            System.out.println("hidden " + hidden + " alpha "+ alpha+ " momentum "+ momentum + " inputs "+ nr_inputs);
            String location = "D:\\Users\\Lydia\\results_nn\\"+sub_folder+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+" "+Integer.toString(hidden)+run_suffix;
            new File(location).mkdirs();
            save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, hidden, alpha, momentum);

            SMR_networks.superSimple(d, location, nr_inputs, nr_categories, hidden, max_it, alpha, momentum);
        }
        
        
        
    }
    
    private static void save_settings(String location, String data, int nr_inputs, int window_size, int nr_categories, int max_it, int nr_hidden, double alpha, double momentum) {
        try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(location+"\\settings_run.txt")))) {
            out.print("Used data "+data+"\n");
            out.print("Nr of inputs "+Integer.toString(nr_inputs)+"\n");
            out.print("Window size "+Integer.toString(window_size)+"\n");
            out.print("Nr of categories "+Integer.toString(nr_categories)+"\n");
            out.print("Max nr iterations "+Integer.toString(max_it)+"\n");
            out.print("Nr hidden nodes "+Integer.toString(nr_hidden)+"\n");
            out.print("Alpha "+Double.toString(alpha)+"\n");
            out.print("Momentum "+Double.toString(momentum)+"\n");
            
        }catch (IOException e) {System.out.println("Exception in write to log smr networks");}
    }
    
    public static void experiment_classes(String run_suffix, String folder_name){
        
//        System.out.println("WAIT A LONG TIME");
//        try {
//            Thread.sleep(5400000);
//        } catch (InterruptedException ex) {
//            Logger.getLogger(Thesis_NN.class.getName()).log(Level.SEVERE, null, ex);
//        }
//        System.out.println("Start experiments");
        
        DataKeeper d = new DataKeeper();
        
        int nr_days = 5;
        int max_it = 100;
        
        int n = 1500000;
        int n_other = 100000;
        
        int window_size=5;
        int nr_categories = 6;
        int nr_inputs = window_size*window_size*nr_days; 
        new File("D:\\Users\\Lydia\\results_nn\\"+folder_name).mkdirs();
        String devision_file = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\division_experiment_diff_sample_types_"+run_suffix+".txt";
        
        int nr_hidden = 40;  
        double alpha = 0.0005;
        double momentum = 0.005;
        
        System.out.println("==========\nnot running exp 1 to save division\n==========");
        String case_name = "politics_lim_ns_o2_logas_hub";
        String data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
//        d.load_Data(data, nr_inputs, nr_categories, n-(2*n_other), n_other, devision_file);                          
        System.out.println("\n\n exp 1");
        String location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        
//        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);
        
                
        System.out.println("\n\n exp 2");
        int nr_inputs_timeind = nr_inputs+12+7;
        case_name = "politics_lim_ns_o2_logas_hub_timeind";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;
//        d.load_data_with_division(data, nr_inputs_timeind, nr_categories, devision_file);        
        new File(location).mkdirs();   
        save_settings(location, data, nr_inputs_timeind, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs_timeind+"\n"+data+"\n"+location);
        
//        SMR_networks.superSimple(d, location, nr_inputs_timeind, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        System.out.println("\n\n exp 3");
        case_name = "politics_lim_ns_o2_logas_no_hub";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;;       
//        d.load_data_with_division(data, nr_inputs, nr_categories, devision_file);               
        new File(location).mkdirs();   
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        
//        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);
        
              
        
        System.out.println("\n\n exp RANDOM 4");
        case_name = "politics_lim_ns_random_o2_logas_hub";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;;       
//        d.load_data_with_division(data, nr_inputs, nr_categories, devision_file);        
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        
//        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        System.out.println("\n\n exp 5");
        case_name = "politics_lim_ns_o2_logas_hub_tarind5";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;;       
        int nr_inputs_tarind = nr_inputs+(6*nr_days);
//        d.load_data_with_division(data, nr_inputs_tarind, nr_categories, devision_file);                        
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs_tarind, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs_tarind+"\n"+data+"\n"+location);
        
//        SMR_networks.superSimple(d, location, nr_inputs_tarind, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        System.out.println("\n\n exp 6");
        case_name = "politics_lim_ns_o2_logas_hub_tarind10";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;;       
        nr_inputs_tarind = nr_inputs+(11*nr_days);
//        d.load_data_with_division(data, nr_inputs_tarind, nr_categories, devision_file);                
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs_tarind, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs_tarind+"\n"+data+"\n"+location);
        
//        SMR_networks.superSimple(d, location, nr_inputs_tarind, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        
        System.out.println("\n\n exp 7");
        case_name = "politics_lim_ns_o2_logas_hub_timeind_tarind5";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;;       
        nr_inputs_tarind = nr_inputs+(6*nr_days)+7+12;
//        d.load_data_with_division(data, nr_inputs_tarind, nr_categories, devision_file);                
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs_tarind, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs_tarind+"\n"+data+"\n"+location);
        
//        SMR_networks.superSimple(d, location, nr_inputs_tarind, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        
        
                
        System.out.println("\n\n exp 8");
        nr_categories = 6;
        window_size=1;
        nr_inputs = window_size*window_size*nr_days;
        nr_hidden = 5;
        case_name = "politics_lim_ns_o0_logas_hub";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;      
//        d.load_data_with_division(data, nr_inputs, nr_categories, devision_file);                
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        
//        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        nr_hidden = 40;
             
        
        System.out.println("\n\n exp 9");
        nr_categories = 6;
        window_size=7;
        nr_inputs = window_size*window_size*nr_days;  
        case_name = "politics_lim_ns_o3_logas_hub";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+run_suffix;       
        d.load_data_with_division(data, nr_inputs, nr_categories, devision_file);                
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        
        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);

              
    }
    
    public static void experiment_politics_names(String suffix, String folder_name_out)
    {
        System.out.println("===========\nPOLITICS NAMES\n===========");
        DataKeeper d = new DataKeeper();
               
        
        int nr_days = 5;
        int max_it = 500;
        
        int n = 7043;
        int n_other = 400;
        
        int window_size=5;
        int nr_categories = 6;
        int nr_inputs = window_size*window_size*nr_days;   
        String devision_file = "D:\\Users\\Lydia\\results_nn\\"+folder_name_out+"\\division_experiment_politics_names_"+suffix+".txt";
        
        int nr_hidden = 40;  
        double alpha = 0.005;
        double momentum = 0.05;
        
        
        String case_name = "politics_names_allDocs_o2_hub2";
        String data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        d.load_Data(data, nr_inputs, nr_categories, n-(2*n_other), n_other, devision_file);                          
        System.out.println("\n\n exp 1 politics names " + suffix);
        String location = "D:\\Users\\Lydia\\results_nn\\"+folder_name_out+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+suffix;
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        
        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        case_name = "politics_names_allDocs_o2_hub_random2";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        d.load_Data(data, nr_inputs, nr_categories, n-(2*n_other), n_other, devision_file);                          
        System.out.println("\n\n exp 2 politics names random "+suffix);
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name_out+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+suffix;
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        
        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        window_size = 1;
        nr_inputs = window_size*window_size*nr_days;
        case_name = "politics_names_allDocs_o0_hub2";
        data = "D:\\Users\\Lydia\\results_freqs\\nn_data\\"+case_name+"\\data.txt";
        d.load_Data(data, nr_inputs, nr_categories, n-(2*n_other), n_other, devision_file);                          
        System.out.println("\n\n exp 3 politics names no context " + suffix);
        location = "D:\\Users\\Lydia\\results_nn\\"+folder_name_out+"\\"+case_name+"_"+Double.toString(alpha)+"_"+Double.toString(momentum)+"_"+Integer.toString(nr_hidden)+"_"+suffix;
        System.out.println("Settings ws= "+window_size+" ouputs="+nr_categories+" inputs="+nr_inputs+"\n"+data+"\n"+location);
        new File(location).mkdirs();
        save_settings(location, data, nr_inputs, window_size, nr_categories, max_it, nr_hidden, alpha, momentum);
        
        SMR_networks.superSimple(d, location, nr_inputs, nr_categories, nr_hidden, max_it, alpha, momentum);
        
        System.out.println("===========\nPOLITICS NAMES Done\n===========");
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        DateFormat dateFormat = new SimpleDateFormat("dd/MM HH:mm:ss");
        Date date = new Date();
        System.out.println(dateFormat.format(date));
      
        
//        String folder_name_out = "poltics_names_allDocs";
//        for(int i =0;i<100;i++)
//        {
//            experiment_politics_names("run"+Integer.toString(i), folder_name_out);            
//        }
            
            
//        try {
//            Thread.sleep(9*1000*60*60);            
//        } catch (InterruptedException ex) {
//            Logger.getLogger(Thesis_NN.class.getName()).log(Level.SEVERE, null, ex);
//        }
//        
//        date = new Date();
//        System.out.println(dateFormat.format(date));  
        
//        String folder_name_out_classes = "politics_real";
//        for(int i =1;i<2;i++)
//        {
//             experiment_classes("run"+Integer.toString(i), folder_name_out_classes);            
//        }
        
        
        int nr_days = 5;
        String run_suffix;
        
        String sub_folder = "param_settings_targetEnc";
        String case_name = "politics_lim_ns_o2_logas_hub_tarind5";
        int ws = 5;
        int inputs = ws*ws*nr_days + nr_days*6;
        for(int i =0;i<5;i++)
        {
            run_suffix = "run"+Integer.toString(i);
            experiment_classes_optimize(case_name, ws, inputs,  sub_folder, run_suffix);              
        }
        
        sub_folder = "param_settings_ws7";
        case_name = "politics_lim_ns_o3_logas_hub";
        ws = 7;
        inputs = ws*ws*nr_days;
        for(int i =0;i<3;i++)
        {
            run_suffix = "run"+Integer.toString(i);
            experiment_classes_optimize(case_name, ws, inputs,  sub_folder, run_suffix);              
        }
        
        
        date = new Date();
        System.out.println(dateFormat.format(date));
      
    }
    
}
