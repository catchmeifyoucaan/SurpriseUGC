import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Loader2, Video, Sparkles, Play, Download } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface Veo3Result {
  success: boolean;
  video: {
    video_url: string;
    duration: number;
    aspect_ratio: string;
    quality: string;
    resolution: string;
    file_size: number;
    generation_time: string;
  };
  timestamp: string;
}

export default function Veo3Generator() {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(15);
  const [aspectRatio, setAspectRatio] = useState('9:16');
  const [style, setStyle] = useState('cinematic');
  const [quality, setQuality] = useState('high');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<Veo3Result | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a video prompt');
      return;
    }

    setIsGenerating(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/veo3-generate', {
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
          quality
        })
      });

      if (!response.ok) {
        throw new Error('Veo3 generation failed');
      }

      const data = await response.json();
      setResult(data);
      toast.success('Veo3 video generated successfully!');
    } catch (error) {
      toast.error('Failed to generate Veo3 video');
      console.error('Veo3 error:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = (url: string) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = `veo3_video_${Date.now()}.mp4`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Video className="h-5 w-5 text-purple-500" />
            Veo3 Video Generator
            <Badge variant="secondary" className="ml-2">Google AI</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Video Prompt</label>
            <Textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the video you want to generate..."
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
                max={60}
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
                  <SelectItem value="ultra_high">Ultra High</SelectItem>
                </SelectContent>
              </Select>
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
                Generating Veo3 Video...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Generate with Veo3
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
              Generated Video
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
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
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
            
            <div className="text-xs text-muted-foreground">
              Generated at: {new Date(result.video.generation_time).toLocaleString()}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}