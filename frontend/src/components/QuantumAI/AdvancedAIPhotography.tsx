import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, Camera, ZoomIn, ZoomOut, Image, Video, Package, Crown, Upload, Sparkles, Download } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface ZoomResult {
  success: boolean;
  zoom_result: {
    original_size: [number, number];
    zoomed_size: [number, number];
    zoom_level: string;
    scale_factor: number;
    output_path: string;
    zoom_description: string;
  };
  timestamp: string;
}

interface UpscaleResult {
  success: boolean;
  upscale_result: {
    original_size: [number, number];
    upscaled_size: [number, number];
    scale_factor: number;
    upscaling_model: string;
    quality: string;
    detail_level: string;
    output_path: string;
  };
  timestamp: string;
}

interface VideoResult {
  success: boolean;
  video_result: {
    photo_size: [number, number];
    video_path: string;
    video_model: string;
    duration: number;
    motion_style: string;
    fps: number;
    quality: string;
  };
  timestamp: string;
}

interface ProductShowcaseResult {
  success: boolean;
  showcase_result: {
    pipeline: string;
    product_photo: string;
    results: any;
    quality_score: number;
  };
  timestamp: string;
}

export default function AdvancedAIPhotography() {
  const [activeTab, setActiveTab] = useState('zoom');
  const [photoPath, setPhotoPath] = useState('');
  const [productPhoto, setProductPhoto] = useState('');
  const [aiModelPhoto, setAiModelPhoto] = useState('');
  
  // Zoom states
  const [zoomLevel, setZoomLevel] = useState('extreme_wide');
  const [aspectRatio, setAspectRatio] = useState('16:9');
  const [enhanceDetails, setEnhanceDetails] = useState(true);
  const [isZooming, setIsZooming] = useState(false);
  const [zoomResult, setZoomResult] = useState<ZoomResult | null>(null);
  
  // Upscale states
  const [upscalingModel, setUpscalingModel] = useState('quantum_upscale');
  const [preserveStyle, setPreserveStyle] = useState(true);
  const [enhanceColors, setEnhanceColors] = useState(true);
  const [isUpscaling, setIsUpscaling] = useState(false);
  const [upscaleResult, setUpscaleResult] = useState<UpscaleResult | null>(null);
  
  // Photo-to-video states
  const [videoModel, setVideoModel] = useState('custom_ai');
  const [duration, setDuration] = useState(10);
  const [motionStyle, setMotionStyle] = useState('cinematic');
  const [includeAudio, setIncludeAudio] = useState(true);
  const [isConverting, setIsConverting] = useState(false);
  const [videoResult, setVideoResult] = useState<VideoResult | null>(null);
  
  // Product integration states
  const [integrationStyle, setIntegrationStyle] = useState('natural');
  const [productPosition, setProductPosition] = useState('hand');
  const [lighting, setLighting] = useState('natural');
  const [background, setBackground] = useState('studio');
  const [isIntegrating, setIsIntegrating] = useState(false);
  const [integrationResult, setIntegrationResult] = useState<any>(null);
  
  // Product showcase states
  const [personName, setPersonName] = useState('');
  const [style, setStyle] = useState('viral');
  const [includeVideo, setIncludeVideo] = useState(true);
  const [includeZoomEffects, setIncludeZoomEffects] = useState(true);
  const [isCreatingShowcase, setIsCreatingShowcase] = useState(false);
  const [showcaseResult, setShowcaseResult] = useState<ProductShowcaseResult | null>(null);

  const handlePhotoUpload = (event: React.ChangeEvent<HTMLInputElement>, setter: (value: string) => void) => {
    const file = event.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setter(url);
    }
  };

  const handleZoomOut = async () => {
    if (!photoPath) {
      toast.error('Please upload a photo first');
      return;
    }

    setIsZooming(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/zoom-out-photo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          photo_path: photoPath,
          zoom_level: zoomLevel,
          target_aspect_ratio: aspectRatio,
          enhance_details: enhanceDetails
        })
      });

      if (!response.ok) {
        throw new Error('Zoom out failed');
      }

      const data = await response.json();
      setZoomResult(data);
      toast.success('Zoom out completed successfully!');
    } catch (error) {
      toast.error('Failed to zoom out');
      console.error('Zoom error:', error);
    } finally {
      setIsZooming(false);
    }
  };

  const handleExtremeUpscale = async () => {
    if (!photoPath) {
      toast.error('Please upload a photo first');
      return;
    }

    setIsUpscaling(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/extreme-upscale-photo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          photo_path: photoPath,
          upscaling_model: upscalingModel,
          preserve_style: preserveStyle,
          enhance_colors: enhanceColors
        })
      });

      if (!response.ok) {
        throw new Error('Extreme upscaling failed');
      }

      const data = await response.json();
      setUpscaleResult(data);
      toast.success('Extreme upscaling completed!');
    } catch (error) {
      toast.error('Failed to upscale photo');
      console.error('Upscale error:', error);
    } finally {
      setIsUpscaling(false);
    }
  };

  const handleConvertToVideo = async () => {
    if (!photoPath) {
      toast.error('Please upload a photo first');
      return;
    }

    setIsConverting(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/convert-photo-to-video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          photo_path: photoPath,
          video_model: videoModel,
          duration: duration,
          motion_style: motionStyle,
          include_audio: includeAudio
        })
      });

      if (!response.ok) {
        throw new Error('Photo-to-video conversion failed');
      }

      const data = await response.json();
      setVideoResult(data);
      toast.success('Photo converted to video successfully!');
    } catch (error) {
      toast.error('Failed to convert photo to video');
      console.error('Conversion error:', error);
    } finally {
      setIsConverting(false);
    }
  };

  const handleProductIntegration = async () => {
    if (!productPhoto || !aiModelPhoto) {
      toast.error('Please upload both product and AI model photos');
      return;
    }

    setIsIntegrating(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/integrate-product-with-ai-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          product_photo: productPhoto,
          ai_model_photo: aiModelPhoto,
          integration_style: integrationStyle,
          product_position: productPosition,
          lighting: lighting,
          background: background
        })
      });

      if (!response.ok) {
        throw new Error('Product integration failed');
      }

      const data = await response.json();
      setIntegrationResult(data);
      toast.success('Product integrated with AI model!');
    } catch (error) {
      toast.error('Failed to integrate product');
      console.error('Integration error:', error);
    } finally {
      setIsIntegrating(false);
    }
  };

  const handleCreateShowcase = async () => {
    if (!productPhoto) {
      toast.error('Please upload a product photo first');
      return;
    }

    setIsCreatingShowcase(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/create-product-showcase', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          product_photo: productPhoto,
          person_name: personName,
          style: style,
          include_video: includeVideo,
          include_zoom_effects: includeZoomEffects
        })
      });

      if (!response.ok) {
        throw new Error('Product showcase creation failed');
      }

      const data = await response.json();
      setShowcaseResult(data);
      toast.success('Product showcase created successfully!');
    } catch (error) {
      toast.error('Failed to create product showcase');
      console.error('Showcase error:', error);
    } finally {
      setIsCreatingShowcase(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Crown className="h-5 w-5 text-purple-600" />
            Advanced AI Photography
            <Badge variant="secondary" className="ml-2">Revolutionary</Badge>
            <Badge variant="destructive" className="ml-1">Beyond Reality</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="zoom">🔍 Zoom Out</TabsTrigger>
              <TabsTrigger value="upscale">✨ Upscale</TabsTrigger>
              <TabsTrigger value="video">🎬 Photo→Video</TabsTrigger>
              <TabsTrigger value="integration">📦 Product+AI</TabsTrigger>
              <TabsTrigger value="showcase">🚀 Showcase</TabsTrigger>
            </TabsList>
            
            <TabsContent value="zoom" className="space-y-4">
              <div>
                <label className="text-sm font-medium">Upload Photo</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <Camera className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handlePhotoUpload(e, setPhotoPath)}
                      className="hidden"
                      id="photo-upload-zoom"
                    />
                    <label htmlFor="photo-upload-zoom" className="cursor-pointer">
                      <Button variant="outline">Upload Photo</Button>
                    </label>
                  </div>
                </div>
                {photoPath && (
                  <div className="mt-4">
                    <img src={photoPath} alt="Uploaded photo" className="w-32 h-32 object-cover rounded" />
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">Zoom Level</label>
                  <Select value={zoomLevel} onValueChange={setZoomLevel}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="macro">🔬 Macro (0.1x)</SelectItem>
                      <SelectItem value="close">📸 Close (0.25x)</SelectItem>
                      <SelectItem value="medium">📱 Medium (0.5x)</SelectItem>
                      <SelectItem value="wide">🏞️ Wide (1.0x)</SelectItem>
                      <SelectItem value="extreme_wide">🌍 Extreme Wide (2.0x)</SelectItem>
                      <SelectItem value="satellite">🛰️ Satellite (5.0x)</SelectItem>
                      <SelectItem value="cosmic">🌌 Cosmic (10.0x)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Aspect Ratio</label>
                  <Select value={aspectRatio} onValueChange={setAspectRatio}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="16:9">16:9 (Landscape)</SelectItem>
                      <SelectItem value="9:16">9:16 (Portrait)</SelectItem>
                      <SelectItem value="1:1">1:1 (Square)</SelectItem>
                      <SelectItem value="4:3">4:3 (Classic)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="enhanceDetails"
                    checked={enhanceDetails}
                    onChange={(e) => setEnhanceDetails(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="enhanceDetails" className="text-sm font-medium">
                    Enhance Details
                  </label>
                </div>
              </div>

              <Button 
                onClick={handleZoomOut} 
                disabled={isZooming || !photoPath}
                className="w-full"
              >
                {isZooming ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Zooming Out...
                  </>
                ) : (
                  <>
                    <ZoomOut className="mr-2 h-4 w-4" />
                    Zoom Out with AI
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="upscale" className="space-y-4">
              <div>
                <label className="text-sm font-medium">Upload Photo</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <Camera className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handlePhotoUpload(e, setPhotoPath)}
                      className="hidden"
                      id="photo-upload-upscale"
                    />
                    <label htmlFor="photo-upload-upscale" className="cursor-pointer">
                      <Button variant="outline">Upload Photo</Button>
                    </label>
                  </div>
                </div>
                {photoPath && (
                  <div className="mt-4">
                    <img src={photoPath} alt="Uploaded photo" className="w-32 h-32 object-cover rounded" />
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">Upscaling Model</label>
                  <Select value={upscalingModel} onValueChange={setUpscalingModel}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="real_esrgan_4x">Real-ESRGAN 4x</SelectItem>
                      <SelectItem value="real_esrgan_8x">Real-ESRGAN 8x</SelectItem>
                      <SelectItem value="swinir_4x">SwinIR 4x</SelectItem>
                      <SelectItem value="swinir_8x">SwinIR 8x</SelectItem>
                      <SelectItem value="custom_ai_16x">Custom AI 16x</SelectItem>
                      <SelectItem value="quantum_upscale">Quantum Upscale 32x</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="preserveStyle"
                    checked={preserveStyle}
                    onChange={(e) => setPreserveStyle(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="preserveStyle" className="text-sm font-medium">
                    Preserve Style
                  </label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="enhanceColors"
                    checked={enhanceColors}
                    onChange={(e) => setEnhanceColors(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="enhanceColors" className="text-sm font-medium">
                    Enhance Colors
                  </label>
                </div>
              </div>

              <Button 
                onClick={handleExtremeUpscale} 
                disabled={isUpscaling || !photoPath}
                className="w-full"
              >
                {isUpscaling ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Extreme Upscaling...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Extreme Upscale with AI
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="video" className="space-y-4">
              <div>
                <label className="text-sm font-medium">Upload Photo</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <Camera className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handlePhotoUpload(e, setPhotoPath)}
                      className="hidden"
                      id="photo-upload-video"
                    />
                    <label htmlFor="photo-upload-video" className="cursor-pointer">
                      <Button variant="outline">Upload Photo</Button>
                    </label>
                  </div>
                </div>
                {photoPath && (
                  <div className="mt-4">
                    <img src={photoPath} alt="Uploaded photo" className="w-32 h-32 object-cover rounded" />
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="text-sm font-medium">Video Model</label>
                  <Select value={videoModel} onValueChange={setVideoModel}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="gen2">Gen2</SelectItem>
                      <SelectItem value="pika">Pika Labs</SelectItem>
                      <SelectItem value="kwen3">KWEN3</SelectItem>
                      <SelectItem value="custom_ai">Custom AI</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Duration (seconds)</label>
                  <Input
                    type="number"
                    value={duration}
                    onChange={(e) => setDuration(Number(e.target.value))}
                    min={5}
                    max={30}
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium">Motion Style</label>
                  <Select value={motionStyle} onValueChange={setMotionStyle}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="cinematic">Cinematic</SelectItem>
                      <SelectItem value="smooth">Smooth</SelectItem>
                      <SelectItem value="dynamic">Dynamic</SelectItem>
                      <SelectItem value="artistic">Artistic</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="includeAudio"
                    checked={includeAudio}
                    onChange={(e) => setIncludeAudio(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="includeAudio" className="text-sm font-medium">
                    Include Audio
                  </label>
                </div>
              </div>

              <Button 
                onClick={handleConvertToVideo} 
                disabled={isConverting || !photoPath}
                className="w-full"
              >
                {isConverting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Converting to Video...
                  </>
                ) : (
                  <>
                    <Video className="mr-2 h-4 w-4" />
                    Convert Photo to Video
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="integration" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Product Photo</label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                    <Package className="mx-auto h-12 w-12 text-gray-400" />
                    <div className="mt-4">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={(e) => handlePhotoUpload(e, setProductPhoto)}
                        className="hidden"
                        id="product-upload"
                      />
                      <label htmlFor="product-upload" className="cursor-pointer">
                        <Button variant="outline">Upload Product</Button>
                      </label>
                    </div>
                  </div>
                  {productPhoto && (
                    <div className="mt-4">
                      <img src={productPhoto} alt="Product" className="w-32 h-32 object-cover rounded" />
                    </div>
                  )}
                </div>
                
                <div>
                  <label className="text-sm font-medium">AI Model Photo</label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                    <Camera className="mx-auto h-12 w-12 text-gray-400" />
                    <div className="mt-4">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={(e) => handlePhotoUpload(e, setAiModelPhoto)}
                        className="hidden"
                        id="model-upload"
                      />
                      <label htmlFor="model-upload" className="cursor-pointer">
                        <Button variant="outline">Upload AI Model</Button>
                      </label>
                    </div>
                  </div>
                  {aiModelPhoto && (
                    <div className="mt-4">
                      <img src={aiModelPhoto} alt="AI Model" className="w-32 h-32 object-cover rounded" />
                    </div>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="text-sm font-medium">Integration Style</label>
                  <Select value={integrationStyle} onValueChange={setIntegrationStyle}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="natural">Natural</SelectItem>
                      <SelectItem value="dramatic">Dramatic</SelectItem>
                      <SelectItem value="lifestyle">Lifestyle</SelectItem>
                      <SelectItem value="commercial">Commercial</SelectItem>
                      <SelectItem value="creative">Creative</SelectItem>
                      <SelectItem value="viral">Viral</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Product Position</label>
                  <Select value={productPosition} onValueChange={setProductPosition}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="hand">In Hand</SelectItem>
                      <SelectItem value="arm">On Arm</SelectItem>
                      <SelectItem value="shoulder">On Shoulder</SelectItem>
                      <SelectItem value="head">On Head</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Lighting</label>
                  <Select value={lighting} onValueChange={setLighting}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="natural">Natural</SelectItem>
                      <SelectItem value="studio">Studio</SelectItem>
                      <SelectItem value="dramatic">Dramatic</SelectItem>
                      <SelectItem value="soft">Soft</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Background</label>
                  <Select value={background} onValueChange={setBackground}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="studio">Studio</SelectItem>
                      <SelectItem value="outdoor">Outdoor</SelectItem>
                      <SelectItem value="urban">Urban</SelectItem>
                      <SelectItem value="nature">Nature</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button 
                onClick={handleProductIntegration} 
                disabled={isIntegrating || !productPhoto || !aiModelPhoto}
                className="w-full"
              >
                {isIntegrating ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Integrating Product...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Integrate Product with AI Model
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="showcase" className="space-y-4">
              <div>
                <label className="text-sm font-medium">Product Photo</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <Package className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handlePhotoUpload(e, setProductPhoto)}
                      className="hidden"
                      id="showcase-product-upload"
                    />
                    <label htmlFor="showcase-product-upload" className="cursor-pointer">
                      <Button variant="outline">Upload Product</Button>
                    </label>
                  </div>
                </div>
                {productPhoto && (
                  <div className="mt-4">
                    <img src={productPhoto} alt="Product" className="w-32 h-32 object-cover rounded" />
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="text-sm font-medium">Person Name (Optional)</label>
                  <Input
                    value={personName}
                    onChange={(e) => setPersonName(e.target.value)}
                    placeholder="Use personal AI model..."
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium">Style</label>
                  <Select value={style} onValueChange={setStyle}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="natural">Natural</SelectItem>
                      <SelectItem value="dramatic">Dramatic</SelectItem>
                      <SelectItem value="lifestyle">Lifestyle</SelectItem>
                      <SelectItem value="commercial">Commercial</SelectItem>
                      <SelectItem value="creative">Creative</SelectItem>
                      <SelectItem value="viral">Viral</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="includeVideo"
                    checked={includeVideo}
                    onChange={(e) => setIncludeVideo(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="includeVideo" className="text-sm font-medium">
                    Include Video
                  </label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="includeZoomEffects"
                    checked={includeZoomEffects}
                    onChange={(e) => setIncludeZoomEffects(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="includeZoomEffects" className="text-sm font-medium">
                    Zoom Effects
                  </label>
                </div>
              </div>

              <Button 
                onClick={handleCreateShowcase} 
                disabled={isCreatingShowcase || !productPhoto}
                className="w-full"
              >
                {isCreatingShowcase ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating Product Showcase...
                  </>
                ) : (
                  <>
                    <Crown className="mr-2 h-4 w-4" />
                    Create Complete Product Showcase
                  </>
                )}
              </Button>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Results Display */}
      {zoomResult && zoomResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ZoomOut className="h-5 w-5 text-green-500" />
              Zoom Out Result
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{zoomResult.zoom_result.zoom_level}</div>
                <div className="text-sm text-muted-foreground">Zoom Level</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{zoomResult.zoom_result.scale_factor}x</div>
                <div className="text-sm text-muted-foreground">Scale Factor</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{zoomResult.zoom_result.aspect_ratio}</div>
                <div className="text-sm text-muted-foreground">Aspect Ratio</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{zoomResult.zoom_result.enhanced_details ? "Yes" : "No"}</div>
                <div className="text-sm text-muted-foreground">Enhanced</div>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">{zoomResult.zoom_result.zoom_description}</p>
          </CardContent>
        </Card>
      )}

      {upscaleResult && upscaleResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-green-500" />
              Extreme Upscale Result
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{upscaleResult.upscale_result.scale_factor}x</div>
                <div className="text-sm text-muted-foreground">Scale Factor</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{upscaleResult.upscale_result.upscaling_model}</div>
                <div className="text-sm text-muted-foreground">Model</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{upscaleResult.upscale_result.quality}</div>
                <div className="text-sm text-muted-foreground">Quality</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{upscaleResult.upscale_result.detail_level}</div>
                <div className="text-sm text-muted-foreground">Detail Level</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {videoResult && videoResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Video className="h-5 w-5 text-green-500" />
              Photo-to-Video Result
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{videoResult.video_result.duration}s</div>
                <div className="text-sm text-muted-foreground">Duration</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{videoResult.video_result.video_model}</div>
                <div className="text-sm text-muted-foreground">Model</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{videoResult.video_result.fps}</div>
                <div className="text-sm text-muted-foreground">FPS</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{videoResult.video_result.quality}</div>
                <div className="text-sm text-muted-foreground">Quality</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {showcaseResult && showcaseResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Crown className="h-5 w-5 text-green-500" />
              Product Showcase Created
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{showcaseResult.showcase_result.pipeline}</div>
                <div className="text-sm text-muted-foreground">Pipeline</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{(showcaseResult.showcase_result.quality_score * 100).toFixed(1)}%</div>
                <div className="text-sm text-muted-foreground">Quality Score</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{includeVideo ? "Yes" : "No"}</div>
                <div className="text-sm text-muted-foreground">Video Included</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{includeZoomEffects ? "Yes" : "No"}</div>
                <div className="text-sm text-muted-foreground">Zoom Effects</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}