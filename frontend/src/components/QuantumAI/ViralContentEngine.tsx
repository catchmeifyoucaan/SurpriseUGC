import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, MessageSquare, FileText, Rocket, Calendar, Crown, Sparkles, Target, TrendingUp, Zap } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface ViralCaptionResult {
  success: boolean;
  viral_caption: {
    caption: string;
    hook: string;
    cta: string;
    hashtags: string;
    engagement_boosters: string[];
    platform: string;
    content_type: string;
    industry: string;
    viral_score: number;
    optimal_posting_time: string;
    frequency_recommendation: string;
  };
  timestamp: string;
}

interface LandingPageCopyResult {
  success: boolean;
  landing_page_copy: {
    headline: string;
    subheadline: string;
    benefits: string[];
    social_proof: any;
    cta_buttons: any[];
    urgency_elements: string[];
    conversion_optimization: any;
    seo_optimization: any;
  };
  timestamp: string;
}

interface AutoDeliveryResult {
  success: boolean;
  auto_delivery: {
    campaign_id: string;
    delivery_schedule: any;
    targeting: any;
    platform: string;
    content_type: string;
    estimated_reach: number;
    estimated_cost: number;
    optimization_recommendations: string[];
  };
  timestamp: string;
}

interface ContentCalendarResult {
  success: boolean;
  content_calendar: {
    content_strategy: any;
    content_themes: string[];
    posting_schedule: any;
    content_ideas: any[];
    platform_optimization: any;
    viral_potential: number;
    roi_projections: any;
    optimization_tips: string[];
  };
  timestamp: string;
}

export default function ViralContentEngine() {
  const [activeTab, setActiveTab] = useState('caption');
  
  // Viral Caption states
  const [platform, setPlatform] = useState('tiktok');
  const [contentType, setContentType] = useState('tiktok_ad');
  const [industry, setIndustry] = useState('general');
  const [targetAudience, setTargetAudience] = useState('');
  const [customMessage, setCustomMessage] = useState('');
  const [isGeneratingCaption, setIsGeneratingCaption] = useState(false);
  const [captionResult, setCaptionResult] = useState<ViralCaptionResult | null>(null);
  
  // Landing Page Copy states
  const [landingIndustry, setLandingIndustry] = useState('saas');
  const [productInfo, setProductInfo] = useState('');
  const [landingTargetAudience, setLandingTargetAudience] = useState('');
  const [conversionGoal, setConversionGoal] = useState('lead_generation');
  const [isGeneratingCopy, setIsGeneratingCopy] = useState(false);
  const [copyResult, setCopyResult] = useState<LandingPageCopyResult | null>(null);
  
  // Auto Delivery states
  const [contentPath, setContentPath] = useState('');
  const [deliveryPlatform, setDeliveryPlatform] = useState('tiktok');
  const [deliveryContentType, setDeliveryContentType] = useState('tiktok_ad');
  const [deliveryCaption, setDeliveryCaption] = useState('');
  const [isDelivering, setIsDelivering] = useState(false);
  const [deliveryResult, setDeliveryResult] = useState<AutoDeliveryResult | null>(null);
  
  // Content Calendar states
  const [businessType, setBusinessType] = useState('startup');
  const [calendarIndustry, setCalendarIndustry] = useState('saas');
  const [calendarTargetAudience, setCalendarTargetAudience] = useState('');
  const [goals, setGoals] = useState<string[]>(['brand_awareness', 'lead_generation']);
  const [budget, setBudget] = useState(1000);
  const [isGeneratingCalendar, setIsGeneratingCalendar] = useState(false);
  const [calendarResult, setCalendarResult] = useState<ContentCalendarResult | null>(null);

  const handleGenerateViralCaption = async () => {
    if (!targetAudience) {
      toast.error('Please specify target audience');
      return;
    }

    setIsGeneratingCaption(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/generate-viral-caption', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          platform: platform,
          content_type: contentType,
          industry: industry,
          target_audience: targetAudience,
          custom_message: customMessage
        })
      });

      if (!response.ok) {
        throw new Error('Viral caption generation failed');
      }

      const data = await response.json();
      setCaptionResult(data);
      toast.success('Viral caption generated successfully!');
    } catch (error) {
      toast.error('Failed to generate viral caption');
      console.error('Caption error:', error);
    } finally {
      setIsGeneratingCaption(false);
    }
  };

  const handleGenerateLandingPageCopy = async () => {
    if (!productInfo || !landingTargetAudience) {
      toast.error('Please fill in all required fields');
      return;
    }

    setIsGeneratingCopy(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/generate-landing-page-copy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          industry: landingIndustry,
          product_info: { description: productInfo },
          target_audience: landingTargetAudience,
          conversion_goal: conversionGoal
        })
      });

      if (!response.ok) {
        throw new Error('Landing page copy generation failed');
      }

      const data = await response.json();
      setCopyResult(data);
      toast.success('Landing page copy generated!');
    } catch (error) {
      toast.error('Failed to generate landing page copy');
      console.error('Copy error:', error);
    } finally {
      setIsGeneratingCopy(false);
    }
  };

  const handleAutoDeliverContent = async () => {
    if (!contentPath || !deliveryCaption) {
      toast.error('Please provide content path and caption');
      return;
    }

    setIsDelivering(true);
    
    try {
      const deliverySpec = {
        platform: deliveryPlatform,
        content_type: deliveryContentType,
        target_audience: "Gen Z, Millennials (16-35)",
        optimal_posting_time: "7-9 PM, 12-2 PM",
        frequency: "3-5 posts per day",
        ad_spend_range: [50.0, 500.0],
        targeting_parameters: {
          age_range: "16-35",
          interests: ["entrepreneurship", "money", "success", "business"],
          behaviors: ["online_shopping", "social_media_active"],
          locations: ["United States", "Canada", "UK", "Australia"]
        },
        conversion_objectives: ["website_traffic", "conversions", "brand_awareness"]
      };

      const response = await fetch('/api/v1/quantum-ai/auto-deliver-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          content_path: contentPath,
          delivery_spec: deliverySpec,
          caption: deliveryCaption
        })
      });

      if (!response.ok) {
        throw new Error('Auto-delivery failed');
      }

      const data = await response.json();
      setDeliveryResult(data);
      toast.success('Content auto-delivery initiated!');
    } catch (error) {
      toast.error('Failed to auto-deliver content');
      console.error('Delivery error:', error);
    } finally {
      setIsDelivering(false);
    }
  };

  const handleGenerateContentCalendar = async () => {
    if (!calendarTargetAudience) {
      toast.error('Please specify target audience');
      return;
    }

    setIsGeneratingCalendar(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/generate-content-calendar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          business_type: businessType,
          industry: calendarIndustry,
          target_audience: calendarTargetAudience,
          goals: goals,
          budget: budget
        })
      });

      if (!response.ok) {
        throw new Error('Content calendar generation failed');
      }

      const data = await response.json();
      setCalendarResult(data);
      toast.success('Content calendar generated!');
    } catch (error) {
      toast.error('Failed to generate content calendar');
      console.error('Calendar error:', error);
    } finally {
      setIsGeneratingCalendar(false);
    }
  };

  const addGoal = (goal: string) => {
    if (!goals.includes(goal)) {
      setGoals([...goals, goal]);
    }
  };

  const removeGoal = (goal: string) => {
    setGoals(goals.filter(g => g !== goal));
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Crown className="h-5 w-5 text-purple-600" />
            Viral Content Engine
            <Badge variant="secondary" className="ml-2">Revolutionary</Badge>
            <Badge variant="destructive" className="ml-1">Viral Machine</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="caption">📝 Viral Captions</TabsTrigger>
              <TabsTrigger value="landing">🌐 Landing Pages</TabsTrigger>
              <TabsTrigger value="delivery">🚀 Auto-Delivery</TabsTrigger>
              <TabsTrigger value="calendar">📅 Content Calendar</TabsTrigger>
            </TabsList>
            
            <TabsContent value="caption" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Platform</label>
                  <Select value={platform} onValueChange={setPlatform}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="tiktok">TikTok</SelectItem>
                      <SelectItem value="instagram">Instagram</SelectItem>
                      <SelectItem value="facebook">Facebook</SelectItem>
                      <SelectItem value="youtube">YouTube</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Content Type</label>
                  <Select value={contentType} onValueChange={setContentType}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="tiktok_ad">TikTok Ad</SelectItem>
                      <SelectItem value="instagram_ad">Instagram Ad</SelectItem>
                      <SelectItem value="facebook_ad">Facebook Ad</SelectItem>
                      <SelectItem value="youtube_ad">YouTube Ad</SelectItem>
                      <SelectItem value="organic_social">Organic Social</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Industry</label>
                  <Select value={industry} onValueChange={setIndustry}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="general">General</SelectItem>
                      <SelectItem value="ecommerce">E-commerce</SelectItem>
                      <SelectItem value="saas">SaaS</SelectItem>
                      <SelectItem value="coaching">Coaching</SelectItem>
                      <SelectItem value="real_estate">Real Estate</SelectItem>
                      <SelectItem value="fitness">Fitness</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Target Audience</label>
                  <Input
                    value={targetAudience}
                    onChange={(e) => setTargetAudience(e.target.value)}
                    placeholder="e.g., Gen Z entrepreneurs, 25-35 business owners"
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">Custom Message (Optional)</label>
                <Textarea
                  value={customMessage}
                  onChange={(e) => setCustomMessage(e.target.value)}
                  placeholder="Add your custom message here..."
                  rows={3}
                />
              </div>

              <Button 
                onClick={handleGenerateViralCaption} 
                disabled={isGeneratingCaption || !targetAudience}
                className="w-full"
              >
                {isGeneratingCaption ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Viral Caption...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Generate Viral Caption
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="landing" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Industry</label>
                  <Select value={landingIndustry} onValueChange={setLandingIndustry}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="saas">SaaS</SelectItem>
                      <SelectItem value="ecommerce">E-commerce</SelectItem>
                      <SelectItem value="coaching">Coaching</SelectItem>
                      <SelectItem value="real_estate">Real Estate</SelectItem>
                      <SelectItem value="fitness">Fitness</SelectItem>
                      <SelectItem value="consulting">Consulting</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Conversion Goal</label>
                  <Select value={conversionGoal} onValueChange={setConversionGoal}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="lead_generation">Lead Generation</SelectItem>
                      <SelectItem value="sales">Sales</SelectItem>
                      <SelectItem value="signups">Signups</SelectItem>
                      <SelectItem value="consultation_bookings">Consultation Bookings</SelectItem>
                      <SelectItem value="product_purchases">Product Purchases</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">Product/Service Description</label>
                <Textarea
                  value={productInfo}
                  onChange={(e) => setProductInfo(e.target.value)}
                  placeholder="Describe your product or service..."
                  rows={4}
                />
              </div>

              <div>
                <label className="text-sm font-medium">Target Audience</label>
                <Input
                  value={landingTargetAudience}
                  onChange={(e) => setLandingTargetAudience(e.target.value)}
                  placeholder="e.g., Small business owners, 30-50, tech-savvy"
                />
              </div>

              <Button 
                onClick={handleGenerateLandingPageCopy} 
                disabled={isGeneratingCopy || !productInfo || !landingTargetAudience}
                className="w-full"
              >
                {isGeneratingCopy ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Landing Page Copy...
                  </>
                ) : (
                  <>
                    <FileText className="mr-2 h-4 w-4" />
                    Generate Landing Page Copy
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="delivery" className="space-y-4">
              <div>
                <label className="text-sm font-medium">Content Path</label>
                <Input
                  value={contentPath}
                  onChange={(e) => setContentPath(e.target.value)}
                  placeholder="Path to your video/image content"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Platform</label>
                  <Select value={deliveryPlatform} onValueChange={setDeliveryPlatform}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="tiktok">TikTok</SelectItem>
                      <SelectItem value="instagram">Instagram</SelectItem>
                      <SelectItem value="facebook">Facebook</SelectItem>
                      <SelectItem value="youtube">YouTube</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Content Type</label>
                  <Select value={deliveryContentType} onValueChange={setDeliveryContentType}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="tiktok_ad">TikTok Ad</SelectItem>
                      <SelectItem value="instagram_ad">Instagram Ad</SelectItem>
                      <SelectItem value="facebook_ad">Facebook Ad</SelectItem>
                      <SelectItem value="youtube_ad">YouTube Ad</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">Caption</label>
                <Textarea
                  value={deliveryCaption}
                  onChange={(e) => setDeliveryCaption(e.target.value)}
                  placeholder="Enter your caption for auto-delivery..."
                  rows={3}
                />
              </div>

              <Button 
                onClick={handleAutoDeliverContent} 
                disabled={isDelivering || !contentPath || !deliveryCaption}
                className="w-full"
              >
                {isDelivering ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Auto-Delivering Content...
                  </>
                ) : (
                  <>
                    <Rocket className="mr-2 h-4 w-4" />
                    Auto-Deliver Content
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="calendar" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Business Type</label>
                  <Select value={businessType} onValueChange={setBusinessType}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="startup">Startup</SelectItem>
                      <SelectItem value="established_business">Established Business</SelectItem>
                      <SelectItem value="agency">Agency</SelectItem>
                      <SelectItem value="consultant">Consultant</SelectItem>
                      <SelectItem value="creator">Content Creator</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Industry</label>
                  <Select value={calendarIndustry} onValueChange={setCalendarIndustry}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="saas">SaaS</SelectItem>
                      <SelectItem value="ecommerce">E-commerce</SelectItem>
                      <SelectItem value="coaching">Coaching</SelectItem>
                      <SelectItem value="real_estate">Real Estate</SelectItem>
                      <SelectItem value="fitness">Fitness</SelectItem>
                      <SelectItem value="consulting">Consulting</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">Target Audience</label>
                <Input
                  value={calendarTargetAudience}
                  onChange={(e) => setCalendarTargetAudience(e.target.value)}
                  placeholder="e.g., Small business owners, 25-45, tech-savvy"
                />
              </div>

              <div>
                <label className="text-sm font-medium">Goals</label>
                <div className="flex flex-wrap gap-2 mb-2">
                  {goals.map((goal) => (
                    <Badge key={goal} variant="secondary" className="cursor-pointer" onClick={() => removeGoal(goal)}>
                      {goal.replace('_', ' ')} ×
                    </Badge>
                  ))}
                </div>
                <div className="flex flex-wrap gap-2">
                  {['brand_awareness', 'lead_generation', 'sales', 'engagement', 'traffic'].map((goal) => (
                    <Button
                      key={goal}
                      variant="outline"
                      size="sm"
                      onClick={() => addGoal(goal)}
                      disabled={goals.includes(goal)}
                    >
                      + {goal.replace('_', ' ')}
                    </Button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">Monthly Budget ($)</label>
                <Input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  min={100}
                  max={10000}
                  step={100}
                />
              </div>

              <Button 
                onClick={handleGenerateContentCalendar} 
                disabled={isGeneratingCalendar || !calendarTargetAudience}
                className="w-full"
              >
                {isGeneratingCalendar ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Content Calendar...
                  </>
                ) : (
                  <>
                    <Calendar className="mr-2 h-4 w-4" />
                    Generate Content Calendar
                  </>
                )}
              </Button>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Results Display */}
      {captionResult && captionResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-green-500" />
              Viral Caption Generated
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold mb-2">Full Caption:</h4>
              <p className="text-sm whitespace-pre-wrap">{captionResult.viral_caption.caption}</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <h4 className="font-semibold text-sm">Hook:</h4>
                <p className="text-sm text-muted-foreground">{captionResult.viral_caption.hook}</p>
              </div>
              <div>
                <h4 className="font-semibold text-sm">CTA:</h4>
                <p className="text-sm text-muted-foreground">{captionResult.viral_caption.cta}</p>
              </div>
              <div>
                <h4 className="font-semibold text-sm">Viral Score:</h4>
                <p className="text-sm text-muted-foreground">{(captionResult.viral_caption.viral_score * 100).toFixed(1)}%</p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold text-sm">Optimal Posting Time:</h4>
                <p className="text-sm text-muted-foreground">{captionResult.viral_caption.optimal_posting_time}</p>
              </div>
              <div>
                <h4 className="font-semibold text-sm">Frequency:</h4>
                <p className="text-sm text-muted-foreground">{captionResult.viral_caption.frequency_recommendation}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {copyResult && copyResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-green-500" />
              Landing Page Copy Generated
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold mb-2">Headline:</h4>
              <p className="text-lg font-bold">{copyResult.landing_page_copy.headline}</p>
            </div>
            
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold mb-2">Subheadline:</h4>
              <p className="text-sm">{copyResult.landing_page_copy.subheadline}</p>
            </div>
            
            <div>
              <h4 className="font-semibold text-sm mb-2">Benefits:</h4>
              <ul className="space-y-1">
                {copyResult.landing_page_copy.benefits.map((benefit, index) => (
                  <li key={index} className="text-sm text-muted-foreground">• {benefit}</li>
                ))}
              </ul>
            </div>
          </CardContent>
        </Card>
      )}

      {deliveryResult && deliveryResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Rocket className="h-5 w-5 text-green-500" />
              Content Auto-Delivery Initiated
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{deliveryResult.auto_delivery.platform}</div>
                <div className="text-sm text-muted-foreground">Platform</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{deliveryResult.auto_delivery.estimated_reach.toLocaleString()}</div>
                <div className="text-sm text-muted-foreground">Estimated Reach</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">${deliveryResult.auto_delivery.estimated_cost}</div>
                <div className="text-sm text-muted-foreground">Estimated Cost</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{deliveryResult.auto_delivery.campaign_id}</div>
                <div className="text-sm text-muted-foreground">Campaign ID</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {calendarResult && calendarResult.success && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-green-500" />
              Content Calendar Generated
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-lg font-semibold">{(calendarResult.content_calendar.viral_potential * 100).toFixed(1)}%</div>
                <div className="text-sm text-muted-foreground">Viral Potential</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{calendarResult.content_calendar.content_themes.length}</div>
                <div className="text-sm text-muted-foreground">Content Themes</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{calendarResult.content_calendar.content_ideas.length}</div>
                <div className="text-sm text-muted-foreground">Content Ideas</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{calendarResult.content_calendar.optimization_tips.length}</div>
                <div className="text-sm text-muted-foreground">Optimization Tips</div>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-sm mb-2">Content Themes:</h4>
              <div className="flex flex-wrap gap-2">
                {calendarResult.content_calendar.content_themes.map((theme, index) => (
                  <Badge key={index} variant="outline">{theme}</Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}