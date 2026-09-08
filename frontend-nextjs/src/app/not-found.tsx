import Link from 'next/link';
import { Layout } from '@/presentation/components/common/Layout';

export default function NotFound() {
  return (
    <Layout>
      <div className="min-h-[70vh] flex flex-col items-center justify-center p-6 text-center space-y-6">
        <h1 className="text-8xl font-black text-slate-100 uppercase italic">404</h1>
        <div className="space-y-2">
           <h2 className="text-3xl font-black text-slate-900 uppercase italic tracking-tighter">Content Not Discovered</h2>
           <p className="text-slate-500 font-medium">The requested educational unit could not be located in our archives.</p>
        </div>
        <Link href="/" className="px-8 py-4 bg-slate-900 text-white rounded-2xl font-black uppercase text-xs hover:bg-blue-600 transition-all shadow-xl">
           Return to Dashboard
        </Link>
      </div>
    </Layout>
  );
}
