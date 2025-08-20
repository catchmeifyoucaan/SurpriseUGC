import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Slider } from '@/components/ui/slider';
import { Loader2, Video, Sparkles, Play, Download, Zap, Clock } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface KWEN3Result {
  success: boolean;
  video: {
    video_url: string;
    duration: number;
    aspect_ratio: string;
    quality: string;
    resolution: string;
    file_size: number;
    generation_time: string;
    motion_scale: number;
    model_version: string;
  };
  timestamp: string;
}

export default function KWEN3Generator() {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(15);
  const [aspectRatio, setAspectRatio] = useState('9:16');
  const [style, setStyle] = useState('cinematic');
  const [quality, setQuality] = useState('ultra_hd');
  const [motionScale, setMotionScale] = useState([1.0]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<KWEN3Result | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a video prompt');
      return;
    }

    setIsGenerating(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/kwen3-generate', {
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
          motion_scale: motionScale[0]
        })
      });

      if (!response.ok) {
        throw new Error('KWEN3 generation failed');
      }

      const data = await response.json();
      setResult(data);
      toast.success('KWEN3 video generated successfully!');
    } catch (error) {
      toast.error('Failed to generate KWEN3 video');
      console.error('KWEN3 error:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = (url: string) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = `kwen3_video_${Date.now()}.mp4`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Video className="h-5 w-5 text-purple-600" />
            KWEN3 Video Generator
            <Badge variant="secondary" className="ml-2">Kling AI</Badge>
            <Badge variant="destructive" className="ml-1">Ultra HD</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Video Prompt</label>
            <Textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the video you want to generate with KWEN3..."
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
                  <SelectItem value="21:9">21:9 (Ultrawide)</SelectItem>
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
                  <SelectItem value="artistic">Artistic</SelectItem>
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

          <div>
            <label className="text-sm font-medium">Motion Scale: {motionScale[0]}</label>
            <Slider
              value={motionScale}
              onValueChange={setMotionScale}
              max={2}
              min={0.1}
              step={0.1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-muted-foreground mt-1">
              <span>Subtle</span>
              <span>Dynamic</span>
            </div>
          </div>

          <Button 
            onClick={handleGenerate} 
            disabled={isGenerating}
            className="w-full"
          >
            {isGenerating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating KWEN3 Video...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Generate with KWEN3
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {result && result.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Play className="h-5 w-5 text-green-500" />
              Generated KWEN3 Video
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="aspect-video bg-black rounded-lg overflow-hidden">
              <video
                src={result.video.video_url}
                controls
                className="w-full h-full object-cover"
                poster="/video-placeholder.png"
              >
                Your browser does not support the video tag.
              </video>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{result.video.duration}s</div>
                <div className="text-sm text-muted-foreground">Duration</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{result.video.aspect_ratio}</div>
                <div className="text-sm text-muted-foreground">Aspect Ratio</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{result.video.resolution}</div>
                <div className="text-sm text-muted-foreground">Resolution</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{(result.video.file_size / 1024 / 1024).toFixed(1)}MB</div>
                <div className="text-sm text-muted-foreground">File Size</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{result.video.motion_scale}</div>
                <div className="text-sm text-muted-foreground">Motion Scale</div>
              </div>
            </div>
            
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Zap className="h-4 w-4" />
              <span>Model: {result.video.model_version}</span>
              <Clock className="h-4 w-4 ml-4" />
              <span>Generated: {new Date(result.video.generation_time).toLocaleString()}</span>
            </div>
            
            <div className="flex gap-2">
              <Button 
                onClick={() => handleDownload(result.video.video_url)}
                className="flex-1"
              >
                <Download className="mr-2 h-4 w-4" />
                Download Video
              </Button>
              <Button 
                variant="outline"
                onClick={() => window.open(result.video.video_url, '_blank')}
              >
                <Play className="mr-2 h-4 w-4" />
                Open in New Tab
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}