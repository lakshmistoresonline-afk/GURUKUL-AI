import {
  LayoutGrid,
  Library,
  Bot,
  Video,
  Zap,
  Share2,
  BarChart2
} from 'lucide-react';

export const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutGrid },
  { href: '/library', label: 'Knowledge', icon: Library },
  { href: '/general-learning', label: 'General', icon: Share2 },
  { href: '/tutor', label: 'AI Tutor', icon: Bot },
  { href: '/multimedia', label: 'Visuals', icon: Video },
  { href: '/quiz-hub', label: 'Practice', icon: Zap },
  { href: '/resources', label: 'Catalog', icon: Share2 },
  { href: '/progress', label: 'Analytics', icon: BarChart2 },
];
