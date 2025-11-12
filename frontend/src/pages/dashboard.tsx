/**
 * Main Dashboard
 */

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/router';
import { api } from '@/lib/api';

interface Video {
  id: string;
  title: string;
  script: string;
  status: string;
  video_url?: string;
  thumbnail_url?: string;
  created_at: string;
  views: number;
  clicks: number;
  conversions: number;
}

export default function DashboardPage() {
  const { user, loading: authLoading, isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ totalVideos: 0, totalViews: 0, totalConversions: 0 });

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [videosData, analyticsData] = await Promise.all([
          api.content.getVideos({ limit: 10 }),
          api.analytics.getOverview(),
        ]);

        setVideos(videosData);
        setStats({
          totalVideos: analyticsData.total_videos || 0,
          totalViews: 0,
          totalConversions: 0,
        });
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated) {
      fetchData();
    }
  }, [isAuthenticated]);

  if (authLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">ViralForge.ai</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              {user?.email}
            </span>
            <button
              onClick={logout}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.full_name}!
          </h2>
          <p className="text-gray-600">
            You're on the {user?.role} plan. {user?.videos_generated_this_month} videos generated this month.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm font-medium text-gray-500 mb-1">Total Videos</div>
            <div className="text-3xl font-bold text-gray-900">{user?.videos_generated_total || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm font-medium text-gray-500 mb-1">This Month</div>
            <div className="text-3xl font-bold text-purple-600">{user?.videos_generated_this_month || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm font-medium text-gray-500 mb-1">Plan</div>
            <div className="text-3xl font-bold text-pink-600 capitalize">{user?.role}</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg shadow-lg p-8 mb-8 text-white">
          <h3 className="text-2xl font-bold mb-4">Start Creating</h3>
          <p className="mb-6 opacity-90">
            Generate viral UGC videos powered by AI in minutes
          </p>
          <button
            onClick={() => router.push('/create')}
            className="px-6 py-3 bg-white text-purple-600 font-semibold rounded-lg hover:bg-gray-100 transition"
          >
            Create New Video
          </button>
        </div>

        {/* Recent Videos */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Recent Videos</h3>
          </div>
          <div className="p-6">
            {videos.length === 0 ? (
              <div className="text-center py-12">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                  />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No videos yet</h3>
                <p className="mt-1 text-sm text-gray-500">Get started by creating your first video.</p>
                <div className="mt-6">
                  <button
                    onClick={() => router.push('/create')}
                    className="px-4 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700"
                  >
                    Create Video
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {videos.map((video) => (
                  <div
                    key={video.id}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-purple-300 transition"
                  >
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{video.title}</h4>
                      <p className="text-sm text-gray-500 mt-1">
                        Status: <span className="capitalize">{video.status}</span>
                      </p>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <div className="text-sm font-medium text-gray-900">{video.views} views</div>
                        <div className="text-xs text-gray-500">{video.conversions} conversions</div>
                      </div>
                      {video.video_url && (
                        <button
                          onClick={() => window.open(video.video_url, '_blank')}
                          className="px-3 py-1 bg-purple-100 text-purple-700 text-sm font-medium rounded hover:bg-purple-200"
                        >
                          View
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
