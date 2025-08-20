import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, Brain, Image, Video, Mic, Sync, Type, Crown, Upload, Sparkles, Download } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface TrainingResult {
  success: boolean;
  training: {
    training_id: string;
    person_name: string;
    training_type: string;
    status: string;
    estimated_completion: string;
    model_path: string;
  };
  timestamp: string;
}

interface PersonalVideoResult {
  success: boolean;
  personal_video: {
    pipeline: string;
    person_name: string;
    final_video: string;
    quality_score: number;
    intermediate_results: any;
  };
  timestamp: string;
}

export default function PersonalAITrainer() {
  const [activeTab, setActiveTab] = useState('training');
  const [personName, setPersonName] = useState('');
  const [trainingImages, setTrainingImages] = useState<string[]>([]);
  const [trainingType, setTrainingType] = useState('dreambooth');
  const [customPrompt, setCustomPrompt] = useState('');
  const [trainingSteps, setTrainingSteps] = useState(1000);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingResult, setTrainingResult] = useState<TrainingResult | null>(null);
  
  // Video creation states
  const [videoPrompt, setVideoPrompt] = useState('');
  const [script, setScript] = useState('');
  const [duration, setDuration] = useState(15);
  const [style, setStyle] = useState('cinematic');
  const [includeCaptions, setIncludeCaptions] = useState(true);
  const [isCreatingVideo, setIsCreatingVideo] = useState(false);
  const [videoResult, setVideoResult] = useState<PersonalVideoResult | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    const imageUrls = files.map(file => URL.createObjectURL(file));
    setTrainingImages(prev => [...prev, ...imageUrls]);
  };

  const handleTraining = async () => {
    if (!personName.trim() || trainingImages.length < 10) {
      toast.error('Please provide person name and at least 10 training images');
      return;
    }

    setIsTraining(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/train-personal-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          person_name: personName,
          training_images: trainingImages,
          training_type: trainingType,
          custom_prompt: customPrompt,
          training_steps: trainingSteps
        })
      });

      if (!response.ok) {
        throw new Error('Personal model training failed');
      }

      const data = await response.json();
      setTrainingResult(data);
      toast.success('Personal AI model training started!');
    } catch (error) {
      toast.error('Failed to start training');
      console.error('Training error:', error);
    } finally {
      setIsTraining(false);
    }
  };

  const handleCreateVideo = async () => {
    if (!personName.trim() || !videoPrompt.trim() || !script.trim()) {
      toast.error('Please provide person name, video prompt, and script');
      return;
    }

    setIsCreatingVideo(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/create-personal-video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          prompt: videoPrompt,
          person_name: personName,
          script: script,
          duration: duration,
          style: style,
          include_captions: includeCaptions
        })
      });

      if (!response.ok) {
        throw new Error('Personal video creation failed');
      }

      const data = await response.json();
      setVideoResult(data);
      toast.success('Personal AI video created successfully!');
    } catch (error) {
      toast.error('Failed to create personal video');
      console.error('Video creation error:', error);
    } finally {
      setIsCreatingVideo(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Crown className="h-5 w-5 text-purple-600" />
            Personal AI Trainer
            <Badge variant="secondary" className="ml-2">Enterprise</Badge>
            <Badge variant="destructive" className="ml-1">Revolutionary</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="training">AI Training</TabsTrigger>
              <TabsTrigger value="video">Video Creation</TabsTrigger>
            </TabsList>
            
            <TabsContent value="training" className="space-y-4">
              <div>
                <label className="text-sm font-medium">Person Name</label>
                <Input
                  value={personName}
                  onChange={(e) => setPersonName(e.target.value)}
                  placeholder="Enter the person's name for AI training..."
                />
              </div>

              <div>
                <label className="text-sm font-medium">Training Images (Min 10)</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <input
                      type="file"
                      multiple
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                      id="image-upload"
                    />
                    <label htmlFor="image-upload" className="cursor-pointer">
                      <Button variant="outline">Upload Images</Button>
                    </label>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    Upload at least 10 high-quality images of the person
                  </p>
                </div>
                {trainingImages.length > 0 && (
                  <div className="mt-4">
                    <p className="text-sm text-gray-600 mb-2">
                      Uploaded: {trainingImages.length} images
                    </p>
                    <div className="grid grid-cols-5 gap-2">
                      {trainingImages.map((url, index) => (
                        <img
                          key={index}
                          src={url}
                          alt={`Training image ${index + 1}`}
                          className="w-16 h-16 object-cover rounded"
                        />
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">Training Type</label>
                  <Select value={trainingType} onValueChange={setTrainingType}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="dreambooth">Dreambooth XL</SelectItem>
                      <SelectItem value="kohya">Kohya LoRA</SelectItem>
                      <SelectItem value="custom">Custom Fine-tuned</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Training Steps</label>
                  <Input
                    type="number"
                    value={trainingSteps}
                    onChange={(e) => setTrainingSteps(Number(e.target.value))}
                    min={500}
                    max={2000}
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium">Custom Prompt</label>
                  <Input
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    placeholder="Optional custom training prompt..."
                  />
                </div>
              </div>

              <Button 
                onClick={handleTraining} 
                disabled={isTraining || trainingImages.length < 10}
                className="w-full"
              >
                {isTraining ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Training Personal AI Model...
                  </>
                ) : (
                  <>
                    <Brain className="mr-2 h-4 w-4" />
                    Start AI Training
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="video" className="space-y-4">
              <div>
                <label className="text-sm font-medium">Video Prompt</label>
                <Textarea
                  value={videoPrompt}
                  onChange={(e) => setVideoPrompt(e.target.value)}
                  placeholder="Describe the video you want to generate with the person..."
                  rows={3}
                />
              </div>

              <div>
                <label className="text-sm font-medium">Script</label>
                <Textarea
                  value={script}
                  onChange={(e) => setScript(e.target.value)}
                  placeholder="Enter the script for the person to speak..."
                  rows={4}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">Duration (seconds)</label>
                  <Input
                    type="number"
                    value={duration}
                    onChange={(e) => setDuration(Number(e.target.value))}
                    min={5}
                    max={60}
                  />
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
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="includeCaptions"
                    checked={includeCaptions}
                    onChange={(e) => setIncludeCaptions(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="includeCaptions" className="text-sm font-medium">
                    Include Smart Captions
                  </label>
                </div>
              </div>

              <Button 
                onClick={handleCreateVideo} 
                disabled={isCreatingVideo || !personName.trim() || !videoPrompt.trim() || !script.trim()}
                className="w-full"
              >
                {isCreatingVideo ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating Personal AI Video...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Create Personal AI Video
                  </>
                )}
              </Button>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {trainingResult && trainingResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-green-500" />
              Training Started Successfully
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{trainingResult.training.person_name}</div>
                <div className="text-sm text-muted-foreground">Person</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{trainingResult.training.training_type}</div>
                <div className="text-sm text-muted-foreground">Training Type</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{trainingResult.training.status}</div>
                <div className="text-sm text-muted-foreground">Status</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{trainingResult.training.training_id}</div>
                <div className="text-sm text-muted-foreground">Training ID</div>
              </div>
            </div>
            
            <div className="text-sm text-muted-foreground">
              Estimated completion: {trainingResult.training.estimated_completion}
            </div>
          </CardContent>
        </Card>
      )}

      {videoResult && videoResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Video className="h-5 w-5 text-green-500" />
              Personal AI Video Created
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="aspect-video bg-black rounded-lg overflow-hidden">
              <video
                src={videoResult.personal_video.final_video}
                controls
                className="w-full h-full object-cover"
                poster="/video-placeholder.png"
              >
                Your browser does not support the video tag.
              </video>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{videoResult.personal_video.person_name}</div>
                <div className="text-sm text-muted-foreground">Person</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{videoResult.personal_video.pipeline}</div>
                <div className="text-sm text-muted-foreground">Pipeline</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{(videoResult.personal_video.quality_score * 100).toFixed(1)}%</div>
                <div className="text-sm text-muted-foreground">Quality Score</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{duration}s</div>
                <div className="text-sm text-muted-foreground">Duration</div>
              </div>
            </div>
            
            <div className="flex gap-2">
              <Button 
                onClick={() => window.open(videoResult.personal_video.final_video, '_blank')}
                className="flex-1"
              >
                <Video className="mr-2 h-4 w-4" />
                View Video
              </Button>
              <Button 
                variant="outline"
                onClick={() => {
                  const link = document.createElement('a');
                  link.href = videoResult.personal_video.final_video;
                  link.download = `personal_ai_video_${Date.now()}.mp4`;
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }}
              >
                <Download className="mr-2 h-4 w-4" />
                Download
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}