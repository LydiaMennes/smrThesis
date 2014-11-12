Skip to content
Sign up Sign in This repository
Explore
Features
Enterprise
Blog
 Star 0  Fork 0 josago/ATAA2014
 branch: master  ATAA2014 / tamer-share / src / ataa2014 / NeuralNet.java
lyltjelyltje on 28 Mar sldkfj
3 contributors josagolyltjenicko90
341 lines (286 sloc)  8.524 kb RawBlameHistory   
package ataa2014;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

import org.neuroph.core.data.DataSet;
import org.neuroph.core.data.DataSetRow;
import org.neuroph.core.transfer.TransferFunction;
import org.neuroph.nnet.MultiLayerPerceptron;
import org.neuroph.nnet.learning.*;
import org.rlcommunity.rlglue.codec.types.Action;
import org.rlcommunity.rlglue.codec.types.Observation;

import sun.security.action.GetLongAction;
import edu.utexas.cs.tamerProject.modeling.Sample;
import edu.utexas.cs.tamerProject.modeling.templates.RegressionModel;

/**
 * This class implements a neural network to be used as a regression model to learn the H function within the TAMER framework.
 * @author josago
 */
public class NeuralNet extends RegressionModel
{
	public static double LEARNING_RATE = 0.01;
	public static double MOMENTUM_RATE = 0;
	
	public static double MIN_ERROR      = 0.1;
	public static int    MAX_ITERATIONS = Integer.MAX_VALUE;
	
	public static int 	TRAIN_TIME = 1000 / 6;
	public static boolean RESET_MODEL = false;
	
	private ArrayList<Double>   outputList;
	private ArrayList<double[]> sampleList;
	
	private ArrayList<Double>   countList;
	private ArrayList<Observation> obsList;

	private MultiLayerPerceptron neuralNet;
	
	private final int num_inputs;
	private final int num_hidden;
	
	private Random rand;
	
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
	
	public Action getRandomAction()
	{
		int direction = rand.nextInt(3) - 1;
		int speed = rand.nextInt(2);
		int jump = rand.nextInt(2);
		System.out.println("Random action selected direction: " + direction + " speed: "+speed+" jump: " + jump);
		int[] initAction = {direction, jump, speed};
		Action action = new Action(3, 0);
		action.intArray = initAction;
		return action;
	}
	
	public NeuralNet(int num_inputs, int num_hidden)
	{
		//System.out.println("Initializing neural network with " + num_inputs + " inputs, " + num_hidden + " hidden nodes and 1 output.");
		this.rand = new Random();
		this.num_inputs = num_inputs;
		this.num_hidden = num_hidden;
		
		clearSamplesAndReset();
	}
	
	@Override
	public void addInstance(Sample sample)
	{		
			boolean found = false;
			
			for (int i = 0; i < sampleList.size(); i++)
			{
				if (Arrays.equals(sample.feats, sampleList.get(i)))
				{
					countList.set(i, countList.get(i)+1.0);
					double count = countList.get(i);
					outputList.set(i, ( ((count-1)/count) * outputList.get(i) + (1/count) * sample.label) ); // Weighted average.
					//outputList.set(i, new Double(sample.label)); // Latest value.
					
					found = true;
					break;
				}
			}
			
			if (!found)
			{
				ParamsATAA.epsilon *= 0.99;
				System.out.println("epsilon value: " + ParamsATAA.epsilon);
				sampleList.add(sample.feats);
				outputList.add(new Double(sample.label));
				countList.add(1.0);				
			}
			
			
	}

	@Override
	public void addInstances(Sample[] samples)
	{
		for (Sample s: samples)
		{
			addInstance(s);
		}
	}

	@Override
	public void addInstancesWReplacement(Sample[] samples)
	{
		for (Sample s: samples)
		{
			addInstance(s);
		}
		
	}

	@Override
	public void buildModel()
	{
		DataSet trainingSet = new DataSet(num_inputs, 1);
		
		for (int i = 0; i < sampleList.size(); i++)
		{
			trainingSet.addRow(new DataSetRow(sampleList.get(i), new double[]{outputList.get(i)}));
		}

		if(RESET_MODEL)
		{
			resetNetwork();
		}
				
	    neuralNet.learnInNewThread(trainingSet);		    
	    try
	    {
			Thread.sleep(TRAIN_TIME);
		}
	    catch (InterruptedException e)
		{
	    	
		}		    
	    neuralNet.stopLearning();
	}

	@Override
	public double predictLabel(double[] feats)
	{
		/*for (int i = 0; i < neuralNet.getWeights().length; i++)
		{
			System.out.print(feats[i] + ", ");
			System.out.print(neuralNet.getWeights()[i] + ", ");
		}
		
		System.out.println();*/
		//System.out.println("Neural net contains " + sampleList.size() +" samples");
		
		neuralNet.setInput(feats);
		neuralNet.calculate();
		//System.out.println("Neural network output for the action (" + feats[0] + ", " + feats[1] + ", " + feats[2] + "): " + neuralNet.getOutput()[0]);
		return neuralNet.getOutput()[0];
	}

	@Override
	public void clearSamplesAndReset()
	{
		System.err.println("\nClear samples and reset in Neural Network\n");
		clearSamples();
		resetNetwork();
	}
	
	private void clearSamples()
	{
		outputList = new ArrayList<Double>();
		sampleList = new ArrayList<double[]>();
		countList = new ArrayList<Double>();
		obsList = new ArrayList<Observation>();		
	}
	
	private void resetNetwork()
	{
		neuralNet = new MultiLayerPerceptron(num_inputs, num_hidden, 1);
		
		for (int i = 0; i < num_hidden; i++)
		{
			neuralNet.getLayerAt(1).getNeuronAt(i).setTransferFunction(new Sigmoid(1));
		}

		neuralNet.getLayerAt(2).getNeuronAt(0).setTransferFunction(new Sigmoid(10));
		
		MomentumBackpropagation mbp = new MomentumBackpropagation();
		
		mbp.setMaxError(MIN_ERROR);
		mbp.setLearningRate(LEARNING_RATE);
		mbp.setMomentum(MOMENTUM_RATE);
		mbp.setMaxIterations(MAX_ITERATIONS);
		
		neuralNet.setLearningRule(mbp);
		
		ParamsATAA.epsilon = ParamsATAA.epsilonStartValue;
	}
	
	public void reset()
	{
		System.out.println("Reset neural network");
	}
	
	public void printSamples()
	{
		System.out.println("\n\n\n====================================\nNumber of samples: " + sampleList.size() + "\n\n");
		double diffTotal = 0.0;
		for(int i = 0; i<obsList.size();i++)
		{			
			if(obsList.get(i)!=null)
				System.out.println("observation: " + obsList.get(i).toString());
			else
				System.out.println("No observation available");
			System.out.println("Action: " + sampleList.get(i)[0] + " jump: " + sampleList.get(i)[1] + " speed: "+ sampleList.get(i)[2] + " ");
			System.out.println("Value: " + outputList.get(i));
			System.out.println("Value according to model: " + predictLabel(sampleList.get(i)));
			diffTotal+= Math.abs(outputList.get(i) - predictLabel(sampleList.get(i)));
			
			System.out.println("Values all actions: ");
			for(int d = -1; d<2;d++)
			{
				for(int j = 0; j<2; j++)
				{
					sampleList.get(i)[0] = d;
					sampleList.get(i)[1] = j;
					System.out.println("d: " + sampleList.get(i)[0] + " j: " + sampleList.get(i)[1] + " val: " + predictLabel(sampleList.get(i)) );
				}
			}			
			System.out.println("\n");
		}
		System.out.println("Average error of model: " + (diffTotal/ (double) sampleList.size()) );
		System.out.println("Total error of model: " + diffTotal);
	}
	
	public double[] getStats ()
	{
		/*
		 * Definition statistics
		 * 0 = nr of samples
		 * 1 = average error of model per sample
		 * 2 = average standerd deviation over actions (how discriminative is the model)		 * 
		 */
		double [] stats = new double[3];	
		int nrSamples = sampleList.size();
		
		double diffTotal = 0.0;
		double sdAvg = 0.0;
				
		for(int i = 0; i<nrSamples;i++)
		{			
			//Update total error
			diffTotal+= Math.abs(outputList.get(i) - predictLabel(sampleList.get(i)));
			
			//Calculate standard deviation on actions	
			double sum = 0.0;
			for(int d = -1; d<2;d++)
			{
				for(int j = 0; j<2; j++)
				{
					for(int s = 0; s<2; s++)
					{
						sampleList.get(i)[2] = s;
						sampleList.get(i)[0] = d;
						sampleList.get(i)[1] = j;	
						sum += predictLabel(sampleList.get(i));
					}
				}
			}
			sum = sum/12;
			double sd = 0.0;
			for(int d = -1; d<2;d++)
			{
				for(int j = 0; j<2; j++)
				{
					for(int s = 0; s<2; s++)
					{
						sampleList.get(i)[2] = s;
						sampleList.get(i)[0] = d;
						sampleList.get(i)[1] = j;	
						sd += Math.pow(predictLabel(sampleList.get(i)) - sum, 2);
					}
				}
			}
			sdAvg += Math.sqrt(sd / 12);
		}
		stats[0] = nrSamples;
		stats[1] = diffTotal / nrSamples;
		stats[2] = sdAvg / nrSamples;
		return stats;
	}
	 
}
Status API Training Shop Blog About © 2014 GitHub, Inc. Terms Privacy Security Contact 