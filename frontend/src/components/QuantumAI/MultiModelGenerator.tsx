import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, Video, Sparkles, Play, Download, Zap, Crown, Compare } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface MultiModelResult {
  success: boolean;
  result: {
    best_video: any;
    all_results: Record<string, any>;
    model_used: string;
    ensemble_generation: boolean;
    generation_time: string;
  };
  timestamp: string;
}

interface ModelComparison {
  success: boolean;
  comparison: {
    prompt: string;
    duration: number;
    results: Record<string, any>;
    comparison_time: string;
  };
  timestamp: string;
}

export default function MultiModelGenerator() {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(15);
  const [aspectRatio, setAspectRatio] = useState('9:16');
  const [style, setStyle] = useState('cinematic');
  const [quality, setQuality] = useState('high');
  const [useMultipleModels, setUseMultipleModels] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isComparing, setIsComparing] = useState(false);
  const [result, setResult] = useState<MultiModelResult | null>(null);
  const [comparison, setComparison] = useState<ModelComparison | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a video prompt');
      return;
    }

    setIsGenerating(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/multi-model-generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          prompt,
          duration,
          aspect_ratio: aspectRatio,
          style,
          quality,
          use_multiple_models: useMultipleModels
        })
      });

      if (!response.ok) {
        throw new Error('Multi-model generation failed');
      }

      const data = await response.json();
      setResult(data);
      toast.success('Multi-model video generated successfully!');
    } catch (error) {
      toast.error('Failed to generate multi-model video');
      console.error('Multi-model error:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCompareModels = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a video prompt');
      return;
    }

    setIsComparing(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/compare-models', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          prompt,
          duration
        })
      });

      if (!response.ok) {
        throw new Error('Model comparison failed');
      }

      const data = await response.json();
      setComparison(data);
      toast.success('Model comparison completed!');
    } catch (error) {
      toast.error('Failed to compare models');
      console.error('Comparison error:', error);
    } finally {
      setIsComparing(false);
    }
  };

  const handleDownload = (url: string) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = `multimodel_video_${Date.now()}.mp4`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Crown className="h-5 w-5 text-yellow-500" />
            Multi-Model Video Generator
            <Badge variant="secondary" className="ml-2">Ensemble AI</Badge>
            <Badge variant="destructive" className="ml-1">Best Quality</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Video Prompt</label>
            <Textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the video you want to generate with multiple AI models..."
              rows={4}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="text-sm font-medium">Duration (seconds)</label>
              <Input
                type="number"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                min={5}
                max={120}
              />
            </div>
            
            <div>
              <label className="text-sm font-medium">Aspect Ratio</label>
              <Select value={aspectRatio} onValueChange={setAspectRatio}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="9:16">9:16 (TikTok/Instagram)</SelectItem>
                  <SelectItem value="16:9">16:9 (YouTube)</SelectItem>
                  <SelectItem value="1:1">1:1 (Square)</SelectItem>
                  <SelectItem value="4:3">4:3 (Classic)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <label className="text-sm font-medium">Style</label>
              <Select value={style} onValueChange={setStyle}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cinematic">Cinematic</SelectItem>
                  <SelectItem value="photorealistic">Photorealistic</SelectItem>
                  <SelectItem value="vibrant">Vibrant</SelectItem>
                  <SelectItem value="minimal">Minimal</SelectItem>
                  <SelectItem value="dramatic">Dramatic</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <label className="text-sm font-medium">Quality</label>
              <Select value={quality} onValueChange={setQuality}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="standard">Standard</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="ultra_hd">Ultra HD</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="useMultipleModels"
              checked={useMultipleModels}
              onChange={(e) => setUseMultipleModels(e.target.checked)}
              className="rounded"
            />
            <label htmlFor="useMultipleModels" className="text-sm font-medium">
              Use Multiple Models (Ensemble Generation)
            </label>
          </div>

          <div className="flex gap-2">
            <Button 
              onClick={handleGenerate} 
              disabled={isGenerating}
              className="flex-1"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating with Multi-Model...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Generate Best Video
                </>
              )}
            </Button>
            
            <Button 
              onClick={handleCompareModels}
              disabled={isComparing}
              variant="outline"
            >
              {isComparing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Comparing...
                </>
              ) : (
                <>
                  <Compare className="mr-2 h-4 w-4" />
                  Compare Models
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {result && result.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Crown className="h-5 w-5 text-yellow-500" />
              Best Generated Video ({result.result.model_used.toUpperCase()})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="aspect-video bg-black rounded-lg overflow-hidden">
              <video
                src={result.result.best_video.video_url}
                controls
                className="w-full h-full object-cover"
                poster="/video-placeholder.png"
              >
                Your browser does not support the video tag.
              </video>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{result.result.best_video.duration}s</div>
                <div className="text-sm text-muted-foreground">Duration</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{result.result.best_video.aspect_ratio}</div>
                <div className="text-sm text-muted-foreground">Aspect Ratio</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{result.result.best_video.resolution}</div>
                <div className="text-sm text-muted-foreground">Resolution</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{(result.result.best_video.file_size / 1024 / 1024).toFixed(1)}MB</div>
                <div className="text-sm text-muted-foreground">File Size</div>
              </div>
            </div>
            
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Zap className="h-4 w-4" />
              <span>Model: {result.result.best_video.model}</span>
              <span className="ml-4">Ensemble: {result.result.ensemble_generation ? 'Yes' : 'No'}</span>
            </div>
            
            <div className="flex gap-2">
              <Button 
                onClick={() => handleDownload(result.result.best_video.video_url)}
                className="flex-1"
              >
                <Download className="mr-2 h-4 w-4" />
                Download Best Video
              </Button>
              <Button 
                variant="outline"
                onClick={() => window.open(result.result.best_video.video_url, '_blank')}
              >
                <Play className="mr-2 h-4 w-4" />
                Open in New Tab
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {comparison && comparison.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Compare className="h-5 w-5 text-blue-500" />
              Model Comparison Results
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="overview" className="space-y-4">
              <TabsList>
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="videos">Videos</TabsTrigger>
                <TabsTrigger value="metrics">Metrics</TabsTrigger>
              </TabsList>
              
              <TabsContent value="overview" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {Object.entries(comparison.comparison.results).map(([model, result]) => (
                    <Card key={model}>
                      <CardHeader>
                        <CardTitle className="text-lg capitalize">{model}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span>Success:</span>
                            <Badge variant={result.success ? "default" : "destructive"}>
                              {result.success ? "Yes" : "No"}
                            </Badge>
                          </div>
                          {result.success && (
                            <>
                              <div className="flex justify-between">
                                <span>Quality Score:</span>
                                <span className="font-semibold">
                                  {(result.quality_score * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span>Resolution:</span>
                                <span>{result.resolution}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>File Size:</span>
                                <span>{(result.file_size / 1024 / 1024).toFixed(1)}MB</span>
                              </div>
                            </>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="videos" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(comparison.comparison.results).map(([model, result]) => (
                    result.success && (
                      <Card key={model}>
                        <CardHeader>
                          <CardTitle className="text-lg capitalize">{model} Video</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="aspect-video bg-black rounded-lg overflow-hidden">
                            <video
                              src={result.video_url}
                              controls
                              className="w-full h-full object-cover"
                            >
                              Your browser does not support the video tag.
                            </video>
                          </div>
                        </CardContent>
                      </Card>
                    )
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="metrics" className="space-y-4">
                <div className="space-y-4">
                  {Object.entries(comparison.comparison.results).map(([model, result]) => (
                    result.success && (
                      <Card key={model}>
                        <CardHeader>
                          <CardTitle className="text-lg capitalize">{model} Metrics</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="text-center">
                              <div className="text-lg font-semibold">{(result.quality_score * 100).toFixed(1)}%</div>
                              <div className="text-sm text-muted-foreground">Quality Score</div>
                            </div>
                            <div className="text-center">
                              <div className="text-lg font-semibold">{result.duration}s</div>
                              <div className="text-sm text-muted-foreground">Duration</div>
                            </div>
                            <div className="text-center">
                              <div className="text-lg font-semibold">{result.resolution}</div>
                              <div className="text-sm text-muted-foreground">Resolution</div>
                            </div>
                            <div className="text-center">
                              <div className="text-lg font-semibold">{(result.file_size / 1024 / 1024).toFixed(1)}MB</div>
                              <div className="text-sm text-muted-foreground">File Size</div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    )
                  ))}
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      )}
    </div>
  );
}