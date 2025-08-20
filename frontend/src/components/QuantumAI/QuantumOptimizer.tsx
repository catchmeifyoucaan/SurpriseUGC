import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Zap, Brain, Globe, Users, TrendingUp, Sparkles } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface QuantumOptimizationResult {
  quantum_optimization: {
    optimization_score: number;
    insights: any;
    quantum_state: any;
  };
  style_adaptation: {
    adaptation_score: number;
    style_applied: string;
  };
  performance_prediction: {
    predictions: any;
    confidence_intervals: any;
  };
  emotional_analysis: {
    resonance_score: number;
    emotional_impact_prediction: any;
  };
  overall_score: number;
  processing_timestamp: string;
}

export default function QuantumOptimizer() {
  const [content, setContent] = useState('');
  const [optimizationLevel, setOptimizationLevel] = useState('maximum');
  const [includeEmotionalAnalysis, setIncludeEmotionalAnalysis] = useState(true);
  const [includeTrendPrediction, setIncludeTrendPrediction] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<QuantumOptimizationResult | null>(null);

  const handleOptimize = async () => {
    if (!content.trim()) {
      toast.error('Please enter content to optimize');
      return;
    }

    setIsProcessing(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/optimize-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          content_data: {
            script: content,
            platform: 'tiktok',
            target_audience: 'general'
          },
          optimization_level: optimizationLevel,
          include_emotional_analysis: includeEmotionalAnalysis,
          include_trend_prediction: includeTrendPrediction
        })
      });

      if (!response.ok) {
        throw new Error('Optimization failed');
      }

      const data = await response.json();
      setResult(data);
      toast.success('Content optimized with quantum AI!');
    } catch (error) {
      toast.error('Failed to optimize content');
      console.error('Optimization error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-500" />
            Quantum AI Content Optimizer
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium">Optimization Level</label>
              <Select value={optimizationLevel} onValueChange={setOptimizationLevel}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="basic">Basic</SelectItem>
                  <SelectItem value="advanced">Advanced</SelectItem>
                  <SelectItem value="maximum">Maximum (Quantum)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="emotional"
                checked={includeEmotionalAnalysis}
                onChange={(e) => setIncludeEmotionalAnalysis(e.target.checked)}
              />
              <label htmlFor="emotional" className="text-sm">Emotional Analysis</label>
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="trend"
                checked={includeTrendPrediction}
                onChange={(e) => setIncludeTrendPrediction(e.target.checked)}
              />
              <label htmlFor="trend" className="text-sm">Trend Prediction</label>
            </div>
          </div>

          <div>
            <label className="text-sm font-medium">Content to Optimize</label>
            <Textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter your content here..."
              rows={6}
            />
          </div>

          <Button 
            onClick={handleOptimize} 
            disabled={isProcessing}
            className="w-full"
          >
            {isProcessing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Quantum Processing...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Optimize with Quantum AI
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="quantum">Quantum</TabsTrigger>
            <TabsTrigger value="style">Style</TabsTrigger>
            <TabsTrigger value="performance">Performance</TabsTrigger>
            <TabsTrigger value="emotional">Emotional</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-500" />
                  Overall Optimization Score
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Quantum Score</span>
                    <Badge variant="secondary">
                      {result.quantum_optimization.optimization_score.toFixed(1)}%
                    </Badge>
                  </div>
                  <Progress value={result.quantum_optimization.optimization_score} />
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-500">
                        {result.style_adaptation.adaptation_score.toFixed(1)}%
                      </div>
                      <div className="text-sm text-muted-foreground">Style Adaptation</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-500">
                        {result.emotional_analysis.resonance_score.toFixed(1)}%
                      </div>
                      <div className="text-sm text-muted-foreground">Emotional Resonance</div>
                    </div>
                  </div>

                  <Alert>
                    <AlertDescription>
                      <strong>Overall Score:</strong> {result.overall_score.toFixed(1)}%
                      <br />
                      <strong>Processing Time:</strong> {new Date(result.processing_timestamp).toLocaleString()}
                    </AlertDescription>
                  </Alert>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="quantum" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5 text-purple-500" />
                  Quantum Optimization Insights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium">Viral Potential</h4>
                      <Progress value={result.quantum_optimization.insights.viral_potential * 100} />
                    </div>
                    <div>
                      <h4 className="font-medium">Audience Resonance</h4>
                      <Progress value={result.quantum_optimization.insights.audience_resonance * 100} />
                    </div>
                  </div>
                  
                  <div className="bg-muted p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Quantum State</h4>
                    <pre className="text-xs overflow-auto">
                      {JSON.stringify(result.quantum_optimization.quantum_state, null, 2)}
                    </pre>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="style" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5 text-blue-500" />
                  Neural Style Transfer
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>Style Applied</span>
                    <Badge>{result.style_adaptation.style_applied}</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Adaptation Score</span>
                    <Badge variant="secondary">
                      {result.style_adaptation.adaptation_score.toFixed(1)}%
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="performance" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-500" />
                  Performance Predictions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium">Viral Score</h4>
                      <Progress value={result.performance_prediction.predictions.viral_score * 100} />
                    </div>
                    <div>
                      <h4 className="font-medium">Engagement Rate</h4>
                      <Progress value={result.performance_prediction.predictions.engagement_rate * 100} />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="emotional" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-pink-500" />
                  Emotional Intelligence Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>Emotional Resonance</span>
                    <Badge variant="secondary">
                      {result.emotional_analysis.resonance_score.toFixed(1)}%
                    </Badge>
                  </div>
                  
                  <div className="bg-muted p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Emotional Impact Prediction</h4>
                    <pre className="text-xs overflow-auto">
                      {JSON.stringify(result.emotional_analysis.emotional_impact_prediction, null, 2)}
                    </pre>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}