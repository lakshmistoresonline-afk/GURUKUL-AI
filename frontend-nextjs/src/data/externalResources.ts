export interface ExternalResource {
  id: string;
  title: string;
  description: string;
  organization: string;
  category: 'Textbooks' | 'Videos' | 'Audio' | 'Interactive' | 'Courses' | 'Curriculum' | 'Question Papers';
  url: string;
  icon?: string;
  classLevel?: string;
}

export const QUESTION_PAPER_REPOSITORIES: ExternalResource[] = [
  {
    id: 'ncert-model-papers',
    title: 'NCERT Model Question Papers',
    description: 'Official model question papers and blueprints for primary and middle school.',
    organization: 'NCERT',
    category: 'Question Papers',
    url: 'https://ncert.nic.in/model-question-papers.php',
    classLevel: 'Class 5 & 6'
  },
  {
    id: 'diksha-explore',
    title: 'DIKSHA National Repository',
    description: 'Access the full library of national question banks and assessment items.',
    organization: 'Ministry of Education',
    category: 'Question Papers',
    url: 'https://diksha.gov.in/explore',
    classLevel: 'Class 5 & 6'
  },
  {
    id: 'cbse-academic-sqp',
    title: 'CBSE Sample Papers',
    description: 'Access the official repository of CBSE sample question papers and marking schemes.',
    organization: 'CBSE',
    category: 'Question Papers',
    url: 'https://cbseacademic.nic.in/curriculum_2024-25.html',
    classLevel: 'Class 6 & Above'
  }
];

export const OFFICIAL_PORTALS: ExternalResource[] = [
  {
    id: 'ncert-textbooks',
    title: 'NCERT Textbooks',
    description: 'Official digital versions of NCERT textbooks for all classes.',
    organization: 'NCERT',
    category: 'Textbooks',
    url: 'https://ncert.nic.in/textbook.php'
  },
  {
    id: 'diksha-portal',
    title: 'DIKSHA Portal',
    description: 'National digital infrastructure for teachers and students.',
    organization: 'Ministry of Education',
    category: 'Interactive',
    url: 'https://diksha.gov.in/'
  },
  {
    id: 'cbse-academic',
    title: 'CBSE Academic',
    description: 'Curriculum, sample papers, and academic resources.',
    organization: 'CBSE',
    category: 'Curriculum',
    url: 'https://cbseacademic.nic.in/'
  },
  {
    id: 'swayam',
    title: 'SWAYAM Central',
    description: 'Online courses and certification for secondary and higher education.',
    organization: 'Ministry of Education',
    category: 'Courses',
    url: 'https://swayam.gov.in/'
  }
];

export const SUBJECT_RESOURCES: Record<string, ExternalResource[]> = {
  'mathematics': [
    {
      id: 'ncert-math-solutions',
      title: 'Mathematics Solutions',
      description: 'Step-by-step solutions for NCERT Mathematics problems.',
      organization: 'NCERT',
      category: 'Textbooks',
      url: 'https://ncert.nic.in/exemplar-problems.php'
    }
  ],
  'science': [
    {
      id: 'diksha-home',
      title: 'DIKSHA Science Hub',
      description: 'Interactive science experiments and multimedia resources.',
      organization: 'DIKSHA',
      category: 'Interactive',
      url: 'https://diksha.gov.in/explore'
    }
  ]
};
