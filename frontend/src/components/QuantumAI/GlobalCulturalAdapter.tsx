import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, Globe, Languages, Users, Sparkles } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface CulturalAdaptationResult {
  original_content: any;
  cultural_adaptations: Record<string, any>;
  total_countries: number;
  processing_timestamp: string;
}

export default function GlobalCulturalAdapter() {
  const [content, setContent] = useState('');
  const [selectedCountries, setSelectedCountries] = useState<string[]>(['US', 'IN', 'BR']);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<CulturalAdaptationResult | null>(null);
  const [availableCountries, setAvailableCountries] = useState<string[]>([]);

  useEffect(() => {
    fetchSupportedCountries();
  }, []);

  const fetchSupportedCountries = async () => {
    try {
      const response = await fetch('/api/v1/quantum-ai/supported-countries', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setAvailableCountries(data.supported_countries);
      }
    } catch (error) {
      console.error('Failed to fetch countries:', error);
    }
  };

  const handleAdapt = async () => {
    if (!content.trim()) {
      toast.error('Please enter content to adapt');
      return;
    }

    setIsProcessing(true);
    
    try {
      const response = await fetch('/api/v1/quantum-ai/cultural-adaptation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          content: { script: content },
          target_countries: selectedCountries,
          include_translation: true,
          include_trend_fusion: true
        })
      });

      if (!response.ok) {
        throw new Error('Cultural adaptation failed');
      }

      const data = await response.json();
      setResult(data);
      toast.success(`Content adapted for ${data.total_countries} countries!`);
    } catch (error) {
      toast.error('Failed to adapt content');
      console.error('Adaptation error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const toggleCountry = (country: string) => {
    setSelectedCountries(prev => 
      prev.includes(country) 
        ? prev.filter(c => c !== country)
        : [...prev, country]
    );
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="h-5 w-5 text-blue-500" />
            Global Cultural Adaptation
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Content to Adapt</label>
            <Textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter your content here..."
              rows={4}
            />
          </div>

          <div>
            <label className="text-sm font-medium mb-2 block">Select Target Countries</label>
            <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
              {availableCountries.map(country => (
                <Button
                  key={country}
                  variant={selectedCountries.includes(country) ? "default" : "outline"}
                  size="sm"
                  onClick={() => toggleCountry(country)}
                >
                  {country}
                </Button>
              ))}
            </div>
          </div>

          <Button 
            onClick={handleAdapt} 
            disabled={isProcessing}
            className="w-full"
          >
            {isProcessing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Adapting Content...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Adapt for {selectedCountries.length} Countries
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="adaptations">Adaptations</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Languages className="h-5 w-5 text-green-500" />
                  Adaptation Summary
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-500">
                      {result.total_countries}
                    </div>
                    <div className="text-sm text-muted-foreground">Countries Adapted</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-500">
                      {Object.keys(result.cultural_adaptations).length}
                    </div>
                    <div className="text-sm text-muted-foreground">Successful Adaptations</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="adaptations" className="space-y-4">
            {Object.entries(result.cultural_adaptations).map(([country, adaptation]) => (
              <Card key={country}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5" />
                    {country} - {adaptation.cultural_profile.country}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span>Language</span>
                      <Badge>{adaptation.cultural_profile.language}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Dialect</span>
                      <Badge variant="secondary">{adaptation.cultural_profile.dialect}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Adaptation Score</span>
                      <Badge variant="outline">
                        {(adaptation.cultural_profile.adaptation_score * 100).toFixed(1)}%
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}