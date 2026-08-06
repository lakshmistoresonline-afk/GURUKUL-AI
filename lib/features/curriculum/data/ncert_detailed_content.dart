import '../domain/models/concept_node.dart';

final Map<String, ConceptNode> ncertDetailedContent = {
  // ===========================================================================
  // CLASS 5 MATHEMATICS (Math-Magic)
  // ===========================================================================

  'm5_c1': const ConceptNode(
    id: 'm5_c1',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'The Fish Tale',
    topic: 'Large Numbers',
    subtopic: 'Place Value and Indian System',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: Duration(minutes: 45),
    prerequisites: const [],
    dependencies: const ['m5_c6', 'm6_c1'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Read and write numbers up to 1 crore',
      'Understand lakhs and crores',
      'Use commas in Indian system'
    ],
    examples: const ['Cost of a boat: 12,00,000', 'Distance to moon: 3,84,400 km'],
    misconceptions: const ['Thinking 1 million = 1 crore (it is 10 lakhs)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'How many zeros are in 1 crore?',
        hint: 'Write it down: 1,00,00,000',
        options: ['5', '6', '7', '8'],
        correctAnswer: '7',
        explanation: '1 crore is 100 lakhs. 100 x 1,00,000 = 1,00,00,000.'
      )
    ],
    flashcards: const [
      Flashcard(front: '1 Lakh', back: '100,000 (5 zeros)'),
      Flashcard(front: '1 Crore', back: '1,00,00,000 (7 zeros)')
    ],
    revisionNotes: 'Focus on place value chart: Ones, Thousands, Lakhs, Crores.',
    commonMistakes: const ['Misplacing commas in large numbers'],
    vocabulary: const {
      'Lakh': 'A unit in the Indian numbering system equal to one hundred thousand (1,00,000).',
      'Crore': 'A unit in the Indian numbering system equal to ten million (1,00,00,000).',
      'Place Value': 'The value of a digit based on its position in a number.'
    },
    interactiveActivities: const [
      'Draw a place value chart in your notebook and fill it with the cost of 5 different items.',
      'Find the population of your city and write it in the Indian system using commas.'
    ],
    masteryCheckpoints: const [
      'Can correctly place commas in a 7-digit number.',
      'Can compare two numbers in the lakhs range.',
      'Understands the relationship between Lakh and Million.'
    ]
  ),

  'm5_c2': const ConceptNode(
    id: 'm5_c2',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Shapes and Angles',
    topic: 'Geometry',
    subtopic: 'Types of Angles',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: ['m6_c4'],
    relatedConcepts: [],
    learningObjectives: [
      'Identify Right, Acute, and Obtuse angles',
      'Recognize angles in daily life objects',
      'Understand how shapes change with angles'
    ],
    examples: ['Corner of a book (Right angle)', 'Hands of a clock at 3:00'],
    misconceptions: ['Thinking bigger shapes have bigger angles'],
    practiceExercises: [
      PracticeExercise(
        question: 'An angle smaller than a right angle is called?',
        hint: 'It is a "sharp" angle.',
        options: ['Obtuse', 'Right', 'Acute', 'Straight'],
        correctAnswer: 'Acute',
        explanation: 'Acute angles are less than 90 degrees.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Right Angle', back: '90 degrees (L shape)'),
      Flashcard(front: 'Obtuse Angle', back: 'More than 90, less than 180')
    ],
    revisionNotes: 'Use a "Degree Clock" or Divider to measure angles.',
    commonMistakes: ['Confusing Acute and Obtuse'],
    vocabulary: {
      'Acute Angle': 'An angle that is less than 90 degrees.',
      'Obtuse Angle': 'An angle that is greater than 90 degrees but less than 180 degrees.',
      'Right Angle': 'An angle of exactly 90 degrees.'
    },
    interactiveActivities: [
      'Look around your room and find 5 objects that have a right angle.',
      'Use two pencils to show an angle that is "more than a right angle".'
    ],
    masteryCheckpoints: [
      'Identifies right angles in 2D shapes.',
      'Distinguishes between sharp (acute) and wide (obtuse) corners.',
      'Can use a degree clock to represent a half-right angle.'
    ]
  ),

  'm5_c3': const ConceptNode(
    id: 'm5_c3',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'How Many Squares?',
    topic: 'Measurement',
    subtopic: 'Area and Perimeter',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: ['m5_c11', 'm6_c10'],
    relatedConcepts: [],
    learningObjectives: [
      'Calculate area by counting squares',
      'Understand perimeter as boundary length',
      'Compare areas of different shapes'
    ],
    examples: ['Area of a stamp on a grid', 'Perimeter of a rectangular field'],
    misconceptions: ['Thinking shapes with same area must have same perimeter'],
    practiceExercises: [
      PracticeExercise(
        question: 'If a square has side 3cm, what is its area?',
        hint: 'Count the 1x1 squares inside.',
        options: ['6 sq cm', '9 sq cm', '12 sq cm', '3 sq cm'],
        correctAnswer: '9 sq cm',
        explanation: 'Area of square = side x side = 3 x 3 = 9.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Area', back: 'Space inside a boundary'),
      Flashcard(front: 'Perimeter', back: 'Length of the boundary')
    ],
    revisionNotes: 'Perimeter is sum of all sides. Area is measured in square units.',
    commonMistakes: ['Confusing formulas for area and perimeter']
  ),

  'm5_c4': const ConceptNode(
    id: 'm5_c4',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Parts and Wholes',
    topic: 'Number System',
    subtopic: 'Fractions',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 60),
    prerequisites: [],
    dependencies: ['m6_c7'],
    relatedConcepts: [],
    learningObjectives: [
      'Understand numerator and denominator',
      'Equivalent fractions',
      'Represent fractions on a grid or flag'
    ],
    examples: ['Half an apple (1/2)', 'Three-fourths of a pizza (3/4)'],
    misconceptions: ['Thinking 1/4 is bigger than 1/2 because 4 > 2'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which is an equivalent fraction of 1/2?',
        hint: 'Multiply numerator and denominator by 2.',
        options: ['1/4', '2/4', '1/3', '2/3'],
        correctAnswer: '2/4',
        explanation: '1/2 = (1*2)/(2*2) = 2/4.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Numerator', back: 'Number of parts we have'),
      Flashcard(front: 'Denominator', back: 'Total number of equal parts')
    ],
    revisionNotes: 'Equivalent fractions represent the same amount.',
    commonMistakes: ['Comparing denominators directly without common base']
  ),

  'm5_c5': const ConceptNode(
    id: 'm5_c5',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Does it Look the Same?',
    topic: 'Geometry',
    subtopic: 'Symmetry and Rotations',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Mirror halves and symmetry lines',
      'Half-turn and quarter-turn rotations',
      'Patterns in rotational symmetry'
    ],
    examples: ['Letter H (vertical symmetry)', 'A fan (rotational symmetry)'],
    misconceptions: ['Thinking every shape has a mirror half'],
    practiceExercises: [
      PracticeExercise(
        question: 'If you give a half-turn to the letter "S", does it look the same?',
        hint: 'Rotate your phone upside down.',
        options: ['Yes', 'No'],
        correctAnswer: 'Yes',
        explanation: '"S" looks the same after a 180-degree (half) turn.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Line of Symmetry', back: 'Line that divides a shape into mirror halves'),
      Flashcard(front: 'Half Turn', back: '180 degree rotation')
    ],
    revisionNotes: 'Symmetry is found in nature, letters, and art.',
    commonMistakes: ['Incorrectly identifying lines of symmetry in non-regular shapes']
  ),

  'm5_c6': const ConceptNode(
    id: 'm5_c6',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Be My Multiple, I\'ll be Your Factor',
    topic: 'Number Theory',
    subtopic: 'Multiples and Factors',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.apply,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: ['m5_c1'],
    dependencies: ['m6_c3'],
    relatedConcepts: [],
    learningObjectives: [
      'Find multiples of a number',
      'Identify common multiples and LCM',
      'Find factors and HCF'
    ],
    examples: ['Multiples of 3: 3, 6, 9...', 'Factors of 6: 1, 2, 3, 6'],
    misconceptions: ['Confusing factors with multiples'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the smallest common multiple of 4 and 6?',
        hint: 'List them: 4, 8, 12... and 6, 12...',
        options: ['2', '12', '24', '1'],
        correctAnswer: '12',
        explanation: 'Multiples of 4: 4, 8, 12, 16... Multiples of 6: 6, 12, 18... Smallest common is 12.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Multiple', back: 'Number obtained by multiplying with 1, 2, 3...'),
      Flashcard(front: 'Factor', back: 'Number that divides exactly without remainder')
    ],
    revisionNotes: 'Every number is a factor and multiple of itself. 1 is a factor of every number.',
    commonMistakes: ['Thinking factors are infinite (multiples are infinite)']
  ),

  'm5_c7': const ConceptNode(
    id: 'm5_c7',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Can You See the Pattern?',
    topic: 'Algebraic Thinking',
    subtopic: 'Patterns and Magic Squares',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.create,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Identify number patterns',
      'Create and solve magic squares',
      'Understand rules of rotation in patterns'
    ],
    examples: ['1, 3, 6, 10 (Triangular numbers)', 'Magic Square where all sides sum to 150'],
    misconceptions: ['Patterns only exist in numbers (they exist in shapes too)'],
    practiceExercises: [
      PracticeExercise(
        question: 'In a magic square, the sum of rows, columns, and diagonals is?',
        hint: 'It is always the same.',
        options: ['Different', 'Zero', 'The Same', 'Random'],
        correctAnswer: 'The Same',
        explanation: 'That is what makes it "Magic"!'
      )
    ],
    flashcards: [
      Flashcard(front: 'Palindromes', back: 'Numbers that read the same forwards and backwards (e.g., 121)')
    ],
    revisionNotes: 'Look for the "rule" in every pattern.',
    commonMistakes: ['Incomplete rows in magic squares']
  ),

  'm5_c8': const ConceptNode(
    id: 'm5_c8',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Mapping Your Way',
    topic: 'Spatial Understanding',
    subtopic: 'Scale and Directions',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: ['m6_g4'],
    relatedConcepts: [],
    learningObjectives: [
      'Read maps and identify landmarks',
      'Understand scale (e.g., 1cm = 200km)',
      'Find routes and directions'
    ],
    examples: ['Map of India', 'Route from school to home'],
    misconceptions: ['Thinking distance on map is same as real distance'],
    practiceExercises: [
      PracticeExercise(
        question: 'If scale is 1cm = 10km, how far is 5cm on the map in reality?',
        hint: 'Multiply 5 by 10.',
        options: ['15 km', '50 km', '5 km', '500 km'],
        correctAnswer: '50 km',
        explanation: '5 * 10km = 50km.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Scale', back: 'Ratio of distance on map to real distance')
    ],
    revisionNotes: 'Maps help us find our way. Scaling up or down changes size but not shape.',
    commonMistakes: ['Using wrong multiplication for scale conversion']
  ),

  'm5_c9': const ConceptNode(
    id: 'm5_c9',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Boxes and Sketches',
    topic: 'Geometry',
    subtopic: '3D Shapes and Nets',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: ['m6_c5'],
    relatedConcepts: [],
    learningObjectives: [
      'Identify 3D shapes (Cube, Cylinder, Cone)',
      'Draw floor maps and deep drawings',
      'Understand "Nets" that fold into boxes'
    ],
    examples: ['A dice (Cube)', 'A birthday cap (Cone)'],
    misconceptions: ['Thinking all 2D drawings are "Deep Drawings"'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which of these folds into a cube?',
        hint: 'A cube has 6 square faces.',
        options: ['A T-shaped net with 6 squares', 'A triangle', 'A circle', 'A 5-square net'],
        correctAnswer: 'A T-shaped net with 6 squares',
        explanation: 'A cube needs exactly 6 faces to be complete.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Net', back: '2D shape that can be folded into a 3D box')
    ],
    revisionNotes: 'Nets are like the "clothes" of a 3D shape.',
    commonMistakes: ['Missing faces in a net']
  ),

  'm5_c10': const ConceptNode(
    id: 'm5_c10',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Tenths and Hundredths',
    topic: 'Number System',
    subtopic: 'Decimals',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.understand,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: ['m5_c4'],
    dependencies: ['m6_c8'],
    relatedConcepts: [],
    learningObjectives: [
      'Represent fractions as decimals',
      'Understand tenths (0.1) and hundredths (0.01)',
      'Apply decimals in currency and length'
    ],
    examples: ['10 paise = 0.10 rupee', 'Length of a pencil: 15.5 cm'],
    misconceptions: ['Thinking 0.11 is bigger than 0.2 (0.2 is actually 0.20)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Write 5/100 as a decimal.',
        hint: 'It is five-hundredths.',
        options: ['0.5', '0.05', '5.0', '0.005'],
        correctAnswer: '0.05',
        explanation: 'Division by 100 moves the decimal two places left.'
      )
    ],
    flashcards: [
      Flashcard(front: '1 Tenth', back: '1/10 or 0.1'),
      Flashcard(front: '1 Hundredth', back: '1/100 or 0.01')
    ],
    revisionNotes: 'Decimal point separates the whole number from the fractional part.',
    commonMistakes: ['Incorrect zero placement after decimal']
  ),

  'm5_c11': const ConceptNode(
    id: 'm5_c11',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Area and its Boundary',
    topic: 'Measurement',
    subtopic: 'Advanced Area/Perimeter',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.apply,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['m5_c3'],
    dependencies: ['m6_c10'],
    relatedConcepts: [],
    learningObjectives: [
      'Calculate area of large fields',
      'Word problems on perimeter',
      'Find missing sides given area/perimeter'
    ],
    examples: ['Fencing a garden', 'Dividing a plot into smaller squares'],
    misconceptions: ['Confusing L+B with 2*(L+B)'],
    practiceExercises: [
      PracticeExercise(
        question: 'If perimeter is 20cm and length is 6cm, what is breadth?',
        hint: 'Perimeter = 2*(L+B). So L+B = 10.',
        options: ['4 cm', '14 cm', '10 cm', '2 cm'],
        correctAnswer: '4 cm',
        explanation: '2*(6+B)=20 -> 6+B=10 -> B=4.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Rectangle Area', back: 'Length x Breadth'),
      Flashcard(front: 'Rectangle Perimeter', back: '2 * (Length + Breadth)')
    ],
    revisionNotes: 'Always check the units (cm vs m).',
    commonMistakes: ['Forgetting to multiply by 2 in perimeter']
  ),

  'm5_c12': const ConceptNode(
    id: 'm5_c12',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Smart Charts',
    topic: 'Data Handling',
    subtopic: 'Graphs and Tally Marks',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: ['m6_c9'],
    relatedConcepts: [],
    learningObjectives: [
      'Organize data using Tally Marks',
      'Interpret Bar Graphs and Pie Charts',
      'Growth charts for plants/animals'
    ],
    examples: ['Recording favorite colors of students', 'Rainfall over 5 months'],
    misconceptions: ['Thinking tally marks can only go up to 5'],
    practiceExercises: [
      PracticeExercise(
        question: 'What does a full block of 4 lines with a cross represent in Tally?',
        hint: 'Count the lines.',
        options: ['4', '5', '6', '10'],
        correctAnswer: '5',
        explanation: 'Four vertical lines and one diagonal across them is the standard for 5.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Pie Chart', back: 'Circular chart representing data as parts of a whole')
    ],
    revisionNotes: 'Charts make data easy to understand at a glance.',
    commonMistakes: ['Misreading the scale of a Bar Graph']
  ),

  'm5_c13': const ConceptNode(
    id: 'm5_c13',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Ways to Multiply and Divide',
    topic: 'Operations',
    subtopic: 'Algorithms and Money',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.apply,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 60),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Multiply using box method and standard method',
      'Solve division problems with remainders',
      'Unitary method in daily life'
    ],
    examples: ['Salary calculation', 'Cost of 12 eggs if 1 is 5 rupees'],
    misconceptions: ['Remainder can be bigger than divisor'],
    practiceExercises: [
      PracticeExercise(
        question: 'Divide 450 by 9.',
        hint: '9 times what is 45?',
        options: ['5', '50', '55', '45'],
        correctAnswer: '50',
        explanation: '45/9 = 5, so 450/9 = 50.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Divisor', back: 'The number we divide by'),
      Flashcard(front: 'Quotient', back: 'The result of division')
    ],
    revisionNotes: 'Check division: (Divisor * Quotient) + Remainder = Dividend.',
    commonMistakes: ['Calculation errors in long multiplication']
  ),

  'm5_c14': const ConceptNode(
    id: 'm5_c14',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'How Big? How Heavy?',
    topic: 'Measurement',
    subtopic: 'Volume and Weight',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['m5_c11'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand volume as space occupied',
      'Measure volume of cubes/cuboids',
      'Relationship between volume and water displacement'
    ],
    examples: ['Volume of a box of matchboxes', 'Weight of a coin collection'],
    misconceptions: ['Heavier objects always have more volume'],
    practiceExercises: [
      PracticeExercise(
        question: 'If a cube has side 2cm, what is its volume?',
        hint: 'Volume = side x side x side.',
        options: ['4 cu cm', '6 cu cm', '8 cu cm', '2 cu cm'],
        correctAnswer: '8 cu cm',
        explanation: '2 x 2 x 2 = 8.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Volume', back: 'Space occupied by a 3D object'),
      Flashcard(front: '1 Litre', back: '1000 millilitres')
    ],
    revisionNotes: 'Volume is 3D (L x B x H). Weight is measured in grams and kilograms.',
    commonMistakes: ['Confusing Area (sq) with Volume (cu)']
  ),

  // ===========================================================================
  // CLASS 5 EVS (Looking Around)
  // ===========================================================================

  'e5_c1': const ConceptNode(
    id: 'e5_c1',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Super Senses',
    topic: 'Biology',
    subtopic: 'Animal Senses',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.remember,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: ['s6_c5'],
    relatedConcepts: [],
    learningObjectives: [
      'Describe special senses of animals',
      'Understand how animals communicate',
      'Awareness of tiger conservation'
    ],
    examples: ['Eagles can see 4 times as far as humans', 'Tigers can move their ears to catch sound'],
    misconceptions: ['Animals sleep exactly like humans'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which bird has eyes in front of its head (like humans)?',
        hint: 'It is an nocturnal bird.',
        options: ['Eagle', 'Sparrow', 'Owl', 'Parrot'],
        correctAnswer: 'Owl',
        explanation: 'Owls have eyes in the front of their face, unlike most birds.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Sloth Sleep Time', back: '17 hours a day'),
      Flashcard(front: 'Tiger Roar Distance', back: 'Can be heard 3km away')
    ],
    revisionNotes: 'Focus on Sloth, Tiger, and senses of Ants/Dogs.',
    commonMistakes: ['Thinking all animals see color (most see fewer colors than us)']
  ),

  'e5_c2': const ConceptNode(
    id: 'e5_c2',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'A Snake Charmer’s Story',
    topic: 'Social Studies',
    subtopic: 'Livelihood and Wildlife',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about Kalbeliya community',
      'Understand relationship between humans and animals',
      'Laws regarding wildlife protection'
    ],
    examples: ['Been dance', 'Nagmumphan patterns'],
    misconceptions: ['All snakes are poisonous (only a few are)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which community is famous for snake charming?',
        hint: 'They have a special dance too.',
        options: ['Gonds', 'Kalbeliyas', 'Bheels', 'Santhals'],
        correctAnswer: 'Kalbeliyas',
        explanation: 'Kalbeliyas are a community that used to catch snakes and entertain people.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Poisonous snakes in India', back: 'Cobra, Common Krait, Russel’s Viper, Saw-scaled Viper')
    ],
    revisionNotes: 'Snake charmers help villagers during snake bites and treat snakes as treasures.',
    commonMistakes: ['Thinking snake charmers harm snakes (mostly they care for them)']
  ),

  'e5_c3': const ConceptNode(
    id: 'e5_c3',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'From Tasting to Digesting',
    topic: 'Biology',
    subtopic: 'Digestive System',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: ['s6_c1'],
    relatedConcepts: [],
    learningObjectives: [
      'Identify different taste zones on the tongue',
      'Understand the process of digestion',
      'Importance of a balanced diet and glucose'
    ],
    examples: ['Saliva starting digestion', 'Glucose drip for energy'],
    misconceptions: ['Digestion only happens in the stomach'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the liquid in our mouth that helps in digestion?',
        hint: 'It makes food soft.',
        options: ['Water', 'Acid', 'Saliva', 'Blood'],
        correctAnswer: 'Saliva',
        explanation: 'Saliva breaks down food and makes it easy to swallow.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Stomach Temperature', back: 'About 30°C'),
      Flashcard(front: 'Dr. Beaumont', back: 'Doctor who studied digestion through a hole in a stomach')
    ],
    revisionNotes: 'Chew food well for better digestion. Digestion ends in the intestines.',
    commonMistakes: ['Swallowing food too fast']
  ),

  'e5_c4': const ConceptNode(
    id: 'e5_c4',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Mangoes Round the Year',
    topic: 'Biology',
    subtopic: 'Food Preservation',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn how food gets spoiled',
      'Techniques for preserving food (Drying, Salting, Sugaring)',
      'Story of Mamidi Tandra (Aam Papad)'
    ],
    examples: ['Pickling', 'Refrigeration', 'Milk pasteurization'],
    misconceptions: ['Cooked food never spoils'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is Mamidi Tandra made from?',
        hint: 'It is a king of fruits.',
        options: ['Apple', 'Mango', 'Banana', 'Orange'],
        correctAnswer: 'Mango',
        explanation: 'Mamidi Tandra is the Telugu name for Aam Papad, made from mango pulp.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Preserving Milk', back: 'Boil it'),
      Flashcard(front: 'Preserving Onions', back: 'Keep in dry open place')
    ],
    revisionNotes: 'Check expiry dates on food packets. Glass jars should be dried before pickling.',
    commonMistakes: ['Using wet spoons in pickle jars']
  ),

  'e5_c5': const ConceptNode(
    id: 'e5_c5',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Seeds and Seeds',
    topic: 'Botany',
    subtopic: 'Germination and Dispersal',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: ['s6_c4'],
    relatedConcepts: [],
    learningObjectives: [
      'Conditions required for germination',
      'Methods of seed dispersal (Wind, Water, Animals)',
      'Insectivorous plants (Pitcher plant)'
    ],
    examples: ['Dandelion seeds flying', 'Velcro invented from seeds'],
    misconceptions: ['Seeds need only water to grow (they need air and warmth too)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which plant traps and eats insects?',
        hint: 'It is shaped like a jug.',
        options: ['Cactus', 'Pitcher Plant', 'Rose', 'Peepal'],
        correctAnswer: 'Pitcher Plant',
        explanation: 'Nepenthes (Pitcher plant) traps insects to get nitrogen.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Dispersal by Air', back: 'Light seeds with hair (e.g. Cotton)'),
      Flashcard(front: 'Dispersal by Animals', back: 'Hooks or sticking to fur')
    ],
    revisionNotes: 'Seeds are "sleeping" plants. Sprouted grains are very healthy.',
    commonMistakes: ['Soaking seeds for too long without air']
  ),

  'e5_c6': const ConceptNode(
    id: 'e5_c6',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Every Drop Counts',
    topic: 'Geography',
    subtopic: 'Water Conservation',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Historical water systems (Ghadisar, Stepwells)',
      'Methods of rainwater harvesting',
      'Importance of water for survival'
    ],
    examples: ['Bawris (Stepwells)', 'Rainwater harvesting in Rajasthan'],
    misconceptions: ['Groundwater is infinite'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is a "Bawri"?',
        hint: 'It has steps going down.',
        options: ['A Lake', 'A Stepwell', 'A River', 'A Dam'],
        correctAnswer: 'A Stepwell',
        explanation: 'Stepwells (Bawris) are old systems where steps go deep to reach water.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Al-Biruni', back: 'Traveller from Uzbekistan who wrote about Indian ponds'),
      Flashcard(front: 'Tarun Bharat Sangh', back: 'Group that helps rebuild old lakes')
    ],
    revisionNotes: 'Save water today for a better tomorrow. Reuse water where possible.',
    commonMistakes: ['Leaving taps running']
  ),

  'e5_c7': const ConceptNode(
    id: 'e5_c7',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Experiments with Water',
    topic: 'Physics',
    subtopic: 'Solubility and Floating',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: ['s6_c2'],
    relatedConcepts: [],
    learningObjectives: [
      'Understand what floats and what sinks',
      'Soluble vs Insoluble substances',
      'Evaporation (Dandi March / Salt story)'
    ],
    examples: ['Sugar dissolving in water', 'Oil floating on water'],
    misconceptions: ['Heavy things always sink (a huge ship floats!)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why does a person float in the Dead Sea even if they can\'t swim?',
        hint: 'The water is very salty.',
        options: ['Less salt', 'High salt content', 'Cold water', 'Deep water'],
        correctAnswer: 'High salt content',
        explanation: 'Very salty water makes it easy to float because the water becomes "heavy".'
      )
    ],
    flashcards: [
      Flashcard(front: 'Soluble', back: 'Mixes and disappears in water'),
      Flashcard(front: 'Dandi March', back: 'Mahatma Gandhi’s march in 1930 to protest salt law')
    ],
    revisionNotes: 'Stirring and heating help things dissolve faster.',
    commonMistakes: ['Confusing floating with dissolving']
  ),

  'e5_c8': const ConceptNode(
    id: 'e5_c8',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'A Treat for Mosquitoes',
    topic: 'Biology',
    subtopic: 'Diseases and Prevention',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Identify symptoms of Malaria and Anemia',
      'Lifecycles of mosquitoes and flies',
      'Prevention of mosquito-borne diseases'
    ],
    examples: ['Iron-rich food: Jaggery, Amla, Spinach', 'Mosquito nets'],
    misconceptions: ['Mosquitoes spread Malaria through dirty water (they BREED in water, but bite humans)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which scientist discovered that mosquitoes spread malaria?',
        hint: 'He got a Nobel Prize.',
        options: ['Louis Pasteur', 'Ronald Ross', 'Newton', 'Einstein'],
        correctAnswer: 'Ronald Ross',
        explanation: 'Ronald Ross discovered malaria parasites in the stomach of a mosquito.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Anemia', back: 'Low Hemoglobin or Iron in blood'),
      Flashcard(front: 'Larvae', back: 'Baby mosquitoes (look like threads)')
    ],
    revisionNotes: 'Do not let water collect around your house. Use oil to kill larvae in ponds.',
    commonMistakes: ['Thinking flies spread malaria (they spread stomach infections)']
  ),

  'e5_c9': const ConceptNode(
    id: 'e5_c9',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Up You Go!',
    topic: 'Social Studies',
    subtopic: 'Mountaineering and Leadership',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.remember,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Challenges of mountaineering',
      'Responsibilities of a group leader',
      'Bachendri Pal’s achievement'
    ],
    examples: ['Rappelling', 'Sleeping bags', 'Nylon tents'],
    misconceptions: ['Climbing mountains is only about strength (it is about mental grit too)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who was the first Indian woman to reach Mt. Everest?',
        hint: 'Her story is in the chapter.',
        options: ['Sania Mirza', 'Bachendri Pal', 'P.V. Sindhu', 'Kalpana Chawla'],
        correctAnswer: 'Bachendri Pal',
        explanation: 'Bachendri Pal climbed Mt. Everest in 1984.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Rappelling', back: 'Coming down a mountain using a rope'),
      Flashcard(front: 'Vitamins for climbers', back: 'Vitamin C and Iron for strength/warmth')
    ],
    revisionNotes: 'Leadership means caring for the team and taking the lead when others are tired.',
    commonMistakes: ['Thinking Everest is in India (it is in Nepal/Tibet)']
  ),

  'e5_c10': const ConceptNode(
    id: 'e5_c10',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Walls Tell Stories',
    topic: 'History',
    subtopic: 'Historical Monuments',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: ['ss6_h3'],
    relatedConcepts: [],
    learningObjectives: [
      'Architecture of Golconda Fort',
      'Old systems of water supply in forts',
      'Life in royal palaces vs common people'
    ],
    examples: ['Bastions (Burj)', 'Cannons', 'Museums'],
    misconceptions: ['Old buildings didn\'t have "modern" facilities like pipes'],
    practiceExercises: [
      PracticeExercise(
        question: 'What are the round parts of a fort wall called?',
        hint: 'They are higher than the wall.',
        options: ['Gates', 'Bastions', 'Towers', 'Rooms'],
        correctAnswer: 'Bastions',
        explanation: 'Bastions (Burj) help soldiers see in all directions for safety.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Golconda Fort location', back: 'Hyderabad'),
      Flashcard(front: 'Cannon material', back: 'Bronze (mixture of copper and tin)')
    ],
    revisionNotes: 'Museums help us know how people lived, what they wore, and what they used.',
    commonMistakes: ['Writing on monument walls']
  ),

  'e5_c11': const ConceptNode(
    id: 'e5_c11',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Sunita in Space',
    topic: 'Physics',
    subtopic: 'Gravity and Earth',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: ['ss6_g1'],
    relatedConcepts: [],
    learningObjectives: [
      'Concept of gravity and weightlessness',
      'How Earth looks from space',
      'Life of an astronaut'
    ],
    examples: ['Floating food in space', 'Space shuttle'],
    misconceptions: ['Space has no air (true), so people fall down (false, they float)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why do things fall towards the Earth?',
        hint: 'It is a special pull.',
        options: ['Wind', 'Gravity', 'Magic', 'Magnetism'],
        correctAnswer: 'Gravity',
        explanation: 'Gravity is the force that pulls everything towards the center of the Earth.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Sunita Williams', back: 'Astronaut who spent 6 months in space'),
      Flashcard(front: 'Neil Armstrong', back: 'First man to walk on the moon (1969)')
    ],
    revisionNotes: 'On Earth, gravity keeps our feet on the ground. In space, everything floats!',
    commonMistakes: ['Thinking up and down exist in space']
  ),

  'e5_c12': const ConceptNode(
    id: 'e5_c12',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'What if it Finishes...?',
    topic: 'Natural Resources',
    subtopic: 'Petroleum and Conservation',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand how petroleum is formed',
      'Uses of various oil products (LPG, Kerosene, Petrol)',
      'Ways to save fuel in daily life'
    ],
    examples: ['Traffic jams wasting fuel', 'Solar energy as an alternative'],
    misconceptions: ['Oil is formed very quickly under the earth'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which of these is NOT obtained from petroleum?',
        hint: 'Think about what we get from mines vs forests.',
        options: ['Petrol', 'Diesel', 'Coal', 'Wax'],
        correctAnswer: 'Coal',
        explanation: 'Coal is a solid fossil fuel, while petrol, diesel, and wax are obtained from petroleum.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Adalaj Stepwell location', back: 'Ahmedabad, Gujarat'),
      Flashcard(front: 'Uses of LPG', back: 'Cooking food in homes')
    ],
    revisionNotes: 'Petroleum is called "Black Gold". It takes millions of years to form.',
    commonMistakes: ['Thinking all fuels are petroleum products']
  ),

  'e5_c13': const ConceptNode(
    id: 'e5_c13',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'A Shelter so High!',
    topic: 'Geography',
    subtopic: 'Leh, Ladakh and Tribes',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Lifestyle in high altitude areas (Leh)',
      'About Changpa tribe and Pashmina wool',
      'Types of houses in different terrains'
    ],
    examples: ['Rebo tents', 'Lekha for sheep', 'Pashmina shawls'],
    misconceptions: ['Leh is a hot desert because it is a desert'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the Changpa tribe\'s most precious animal?',
        hint: 'They get wool from it.',
        options: ['Cow', 'Horse', 'Goat', 'Dog'],
        correctAnswer: 'Goat',
        explanation: 'The special goats provide wool for the famous Pashmina shawls.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Cold Desert of India', back: 'Ladakh'),
      Flashcard(front: 'Pashmina Shawl warmth', back: 'As warm as 6 sweaters')
    ],
    revisionNotes: 'Changpa people live at 5000 meters altitude. Their tents are called Rebo.',
    commonMistakes: ['Thinking Changpas live in permanent stone houses']
  ),

  'e5_c14': const ConceptNode(
    id: 'e5_c14',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'When the Earth Shook!',
    topic: 'Geography',
    subtopic: 'Natural Disasters',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understanding earthquakes and their impact',
      'Safety measures during an earthquake',
      'Community help during disasters'
    ],
    examples: ['Kutch earthquake (2001)', 'Building earthquake-resistant houses'],
    misconceptions: ['Earthquakes can be predicted months in advance'],
    practiceExercises: [
      PracticeExercise(
        question: 'What should you do first during an earthquake if you are indoors?',
        hint: 'Protect your head.',
        options: ['Run to the balcony', 'Go under a strong table', 'Use the lift', 'Call friends'],
        correctAnswer: 'Go under a strong table',
        explanation: 'Going under a table protects you from falling objects.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Earthquake help', back: 'Doctors, Army, NGOs, and Neighbors'),
      Flashcard(front: 'Safe place', back: 'Open ground away from buildings')
    ],
    revisionNotes: 'Drop, Cover, and Hold on! Disasters require collective action.',
    commonMistakes: ['Using elevators during an earthquake']
  ),

  'e5_c15': const ConceptNode(
    id: 'e5_c15',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Blow Hot, Blow Cold',
    topic: 'Physics',
    subtopic: 'Respiration and Temperature',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'How breathing helps cool or warm things',
      'Function of a stethoscope',
      'Understanding mirrors fogging up'
    ],
    examples: ['Blowing on hot tea', 'Blowing on cold hands in winter'],
    misconceptions: ['We only breathe out hot air'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why does a mirror become foggy when we breathe on it?',
        hint: 'Our breath has water vapor.',
        options: ['Dust in air', 'Water vapor condensing', 'Mirror is dirty', 'CO2 turning into liquid'],
        correctAnswer: 'Water vapor condensing',
        explanation: 'The moist air from our breath touches the cool mirror and turns into tiny water drops.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Stethoscope', back: 'Instrument used to listen to heartbeat'),
      Flashcard(front: 'Breathing rate', back: 'Increases when we run or exercise')
    ],
    revisionNotes: 'Breath can be used to blow a whistle, cool food, or warm hands.',
    commonMistakes: ['Thinking heartbeat stays the same always']
  ),

  'e5_c16': const ConceptNode(
    id: 'e5_c16',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Who will do this Work?',
    topic: 'Social Studies',
    subtopic: 'Cleanliness and Dignity of Labour',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: ['ss6_c2'],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the importance of cleanliness',
      'Respect all types of work (Dignity of Labour)',
      'Gandhiji\'s views on sanitation'
    ],
    examples: ['Sabarmati Ashram rules', 'Narayan’s childhood story'],
    misconceptions: ['Cleaning is the job of only specific communities'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who said "Every person should do every kind of work"?',
        hint: 'He is the Father of our Nation.',
        options: ['Nehru', 'Gandhiji', 'Ambedkar', 'Patel'],
        correctAnswer: 'Gandhiji',
        explanation: 'Gandhiji believed that no work is low and everyone should clean their own surroundings.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Untouchability', back: 'Unfair practice of treating some people as low'),
      Flashcard(front: 'Bhimrao Ambedkar', back: 'Architect of Indian Constitution who fought against bias')
    ],
    revisionNotes: 'Cleanliness is next to Godliness. Respect everyone who works for us.',
    commonMistakes: ['Thinking certain jobs are "dirty" and should be avoided']
  ),

  'e5_c17': const ConceptNode(
    id: 'e5_c17',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Across the Wall',
    topic: 'Social Studies',
    subtopic: 'Sports and Gender Bias',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 3,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Breaking gender barriers in sports',
      'Importance of teamwork over individual scores',
      'Challenges faced by girl athletes'
    ],
    examples: ['Nagpada Basketball Association', 'Afreen’s story'],
    misconceptions: ['Certain sports are only for boys'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the most important thing in a team?',
        hint: 'Working together.',
        options: ['Individual points', 'Team spirit', 'Famous captain', 'New shoes'],
        correctAnswer: 'Team spirit',
        explanation: 'A team wins when players play for the team, not just for themselves.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Gender Bias', back: 'Treating girls and boys differently/unfairly'),
      Flashcard(front: 'NBA', back: 'Nagpada Basketball Association')
    ],
    revisionNotes: 'Sports help in building confidence and breaking social walls.',
    commonMistakes: ['Focusing only on winning, not playing']
  ),

  'e5_c18': const ConceptNode(
    id: 'e5_c18',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'No Place for Us?',
    topic: 'Social Studies',
    subtopic: 'Migration and Displacement',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Reasons for migration (Dams, Jobs, Education)',
      'Problems faced by displaced people in cities',
      'Village life vs City life'
    ],
    examples: ['Khedi village', 'Jatrya Bhai’s struggle in Mumbai'],
    misconceptions: ['Cities are always a better place to live than villages'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why was Jatrya Bhai forced to leave his village Khedi?',
        hint: 'A big wall was being built on the river.',
        options: ['For fun', 'To build a dam', 'Because of a fire', 'To find gold'],
        correctAnswer: 'To build a dam',
        explanation: 'When dams are built, nearby villages are often submerged, forcing people to move.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Migration', back: 'Moving from one place to another for work or safety'),
      Flashcard(front: 'Displacement', back: 'Being forced to leave one\'s home')
    ],
    revisionNotes: 'Villages have fresh air and community; cities have jobs and schools but are crowded.',
    commonMistakes: ['Thinking all people move to cities by choice']
  ),

  'e5_c19': const ConceptNode(
    id: 'e5_c19',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'A Seed tells a Farmer’s Story',
    topic: 'Agriculture',
    subtopic: 'Traditional vs Modern Farming',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['e5_c5'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Evolution of farming techniques',
      'Chemical fertilizers vs Natural manure',
      'Impact of hybrid seeds and monoculture'
    ],
    examples: ['Undhiya (Gujarati dish)', 'Van-gam village', 'Earthworms as farmer friends'],
    misconceptions: ['Chemical fertilizers are always better for soil'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which animal is called a "friend of farmers"?',
        hint: 'It lives in the soil.',
        options: ['Lion', 'Earthworm', 'Dog', 'Cat'],
        correctAnswer: 'Earthworm',
        explanation: 'Earthworms soften the soil and turn waste into manure.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Undhiya', back: 'A traditional winter vegetable dish cooked upside down'),
      Flashcard(front: 'Hybrid Seeds', back: 'Seeds made in labs that need more water and chemicals')
    ],
    revisionNotes: 'Traditional farming used natural seeds and manure. Modern farming uses machines and chemicals.',
    commonMistakes: ['Thinking tractors are always better than bullocks']
  ),

  'e5_c20': const ConceptNode(
    id: 'e5_c20',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Whose Forests?',
    topic: 'Environment',
    subtopic: 'Conservation and Adivasis',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Importance of forests for Adivasis',
      'Right to Forest Act 2007',
      'Suryamani\'s "Torang" center'
    ],
    examples: ['Kuduk language', 'Cheraw dance', 'Jhum farming'],
    misconceptions: ['Adivasis destroy forests'],
    practiceExercises: [
      PracticeExercise(
        question: 'What does "Torang" mean in Kuduk language?',
        hint: 'It is a place with lots of trees.',
        options: ['Mountain', 'River', 'Jungle', 'Sky'],
        correctAnswer: 'Jungle',
        explanation: 'Suryamani started Torang to preserve Kuduk culture and forests.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Jhum Farming', back: 'Traditional shifting cultivation in Mizoram'),
      Flashcard(front: 'Right to Forest Act', back: 'People living in forests for 25 years have right over the land')
    ],
    revisionNotes: 'Forests are our collective bank. Cheraw is a famous bamboo dance.',
    commonMistakes: ['Thinking Jhum farming is done in plains']
  ),

  'e5_c21': const ConceptNode(
    id: 'e5_c21',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'Like Father, Like Daughter',
    topic: 'Biology',
    subtopic: 'Heredity and Traits',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Identify inherited traits (habits, features)',
      'Understand Gregor Mendel\'s experiments with peas',
      'Adopted vs Biological traits'
    ],
    examples: ['Curly hair', 'Polio (not inherited)', 'Tallness in pea plants'],
    misconceptions: ['Diseases like Polio are inherited from parents'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who did experiments with 28,000 pea plants?',
        hint: 'He was a monk.',
        options: ['Einstein', 'Mendel', 'Darwin', 'Newton'],
        correctAnswer: 'Mendel',
        explanation: 'Gregor Mendel discovered the rules of heredity using pea plants.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Gregor Mendel', back: 'Father of Genetics'),
      Flashcard(front: 'Polio', back: 'Caused by a virus, not inherited from parents')
    ],
    revisionNotes: 'Some traits we get from birth, others we learn from our surroundings.',
    commonMistakes: ['Confusing learned habits with inherited traits']
  ),

  'e5_c22': const ConceptNode(
    id: 'e5_c22',
    subject: 'EVS',
    classLevel: 5,
    chapter: 'On the Move Again',
    topic: 'Social Studies',
    subtopic: 'Livelihood and Loans',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Life of sugarcane workers',
      'Concept of "Mukadam" (agent)',
      'Impact of seasonal migration on children’s education'
    ],
    examples: ['Dhanu’s village', 'Working in sugar factories'],
    misconceptions: ['All farmers have their own land'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is a "Mukadam"?',
        hint: 'He lends money to families.',
        options: ['A Doctor', 'An Agent/Money lender', 'A Teacher', 'A Driver'],
        correctAnswer: 'An Agent/Money lender',
        explanation: 'Mukadams lend money and tell families where they will work for the next few months.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Caravan', back: 'Group of families moving together with their belongings'),
      Flashcard(front: 'Puranpoli', back: 'Sweet rotis made of gram and jaggery')
    ],
    revisionNotes: 'Seasonal work forces families to move, which often disrupts children\'s studies.',
    commonMistakes: ['Thinking farmers work all 12 months on the same crop']
  ),

  // ===========================================================================
  // CLASS 5 ENGLISH (Marigold)
  // ===========================================================================

  'en5_c1': const ConceptNode(
    id: 'en5_c1',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 1: Ice-cream Man / Wonderful Waste!',
    topic: 'Literature and Creative Writing',
    subtopic: 'Vocabulary and Recycling',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.create,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand rhyming words and adjectives',
      'Learn how to recycle household waste',
      'Describe scenes using sensory words'
    ],
    examples: ['Scraps turning into "Avial" dish', 'Trundling, mounds, frosty-fizz'],
    misconceptions: ['Recycling is only for factories (we can do it at home too!)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What dish was made from vegetable scraps in the palace of Travancore?',
        hint: 'It is a famous Kerala dish.',
        options: ['Sambar', 'Avial', 'Dosa', 'Idli'],
        correctAnswer: 'Avial',
        explanation: 'Avial was made by the cook using vegetable bits that were going to be thrown away.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Wonderful Waste', back: 'Idea that waste can be useful if we are creative'),
      Flashcard(front: 'Rhyming with "Sight"', back: 'Bright, Light, Night')
    ],
    revisionNotes: 'Ice-cream man poem focus on imagery. Wonderful Waste story focus on resourcefulness.',
    commonMistakes: ['Spelling of "Wonderful"', 'Confusing adjectives with verbs']
  ),

  'en5_c2': const ConceptNode(
    id: 'en5_c2',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 2: Teamwork / Flying Together',
    topic: 'Value Education',
    subtopic: 'Collaboration and Wisdom',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Importance of working together to achieve goals',
      'Wisdom of elders (Panchatantra-style story)',
      'Learning to follow advice'
    ],
    examples: ['Geese escaping the hunter', 'Passing the ball in basketball'],
    misconceptions: ['One person can do everything alone'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why did the wise old bird tell the other geese to destroy the creeper?',
        hint: 'Creepers grow and become strong.',
        options: ['It was ugly', 'A hunter could climb it', 'It was blocking sun', 'For no reason'],
        correctAnswer: 'A hunter could climb it',
        explanation: 'The wise bird knew that a strong creeper would help a hunter climb the tree.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Teamwork', back: 'Working together to make our dream work'),
      Flashcard(front: 'Unity', back: 'Together we are strong')
    ],
    revisionNotes: 'Listen to advice from those who have more experience.',
    commonMistakes: ['Ignoring the "moral of the story"']
  ),

  'en5_c3': const ConceptNode(
    id: 'en5_c3',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 3: My Shadow / Robinson Crusoe',
    topic: 'Literature',
    subtopic: 'Self-discovery and Adventure',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 60),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Poetic devices in "My Shadow"',
      'Adventure and survival skills',
      'Using imagination in writing'
    ],
    examples: ['Footprint on the sand', 'Shadow growing taller and shorter'],
    misconceptions: ['Robinson Crusoe was never afraid'],
    practiceExercises: [
      PracticeExercise(
        question: 'What did Robinson Crusoe see on the sand that frightened him?',
        hint: 'It belongs to a foot.',
        options: ['A snake', 'A footprint', 'A shell', 'A boat'],
        correctAnswer: 'A footprint',
        explanation: 'He was lonely for years, so a human footprint made him think of savages.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Buttercup', back: 'A yellow flower mentioned in the poem'),
      Flashcard(front: 'Crusoe\'s companion', back: 'He later found a man and named him Friday')
    ],
    revisionNotes: 'Shadows change size based on light position. Crusoe lived on a desert island.',
    commonMistakes: ['Confusing "scared" with "scary"']
  ),

  'en5_c4': const ConceptNode(
    id: 'en5_c4',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 4: Crying / My Elder Brother',
    topic: 'Drama and Emotions',
    subtopic: 'Relationships and Pressure',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Expression of emotions through poetry',
      'Dynamics of siblings and academic expectations',
      'Difference between bookish knowledge and life experience'
    ],
    examples: ['Bhaiya vs Munna', 'Crying until the pillow is soaked'],
    misconceptions: ['Studying all the time is the only way to be wise'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who was three years older but five years ahead in school?',
        hint: 'He studied very hard.',
        options: ['Munna', 'Bhaiya', 'The Father', 'The Teacher'],
        correctAnswer: 'Bhaiya',
        explanation: 'Bhaiya took his studies very seriously but struggled to pass.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Crying', back: 'A way to let out emotions to feel happy later'),
      Flashcard(front: 'Foundation', back: 'Strong base (Bhaiya wanted a strong base in English)')
    ],
    revisionNotes: 'Experience is as important as books. Respect your elders\' wisdom.',
    commonMistakes: ['Thinking Bhaiya was mean (he was actually caring)']
  ),

  'en5_c5': const ConceptNode(
    id: 'en5_c5',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 5: The Lazy Frog / Rip Van Winkle',
    topic: 'Storytelling',
    subtopic: 'Behavior and Time',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Identify traits of laziness',
      'Narrative structure of a legend',
      'Using past tense in storytelling'
    ],
    examples: ['Rip sleeping for 20 years', 'Fred the frog ignoring his mother'],
    misconceptions: ['Rip Van Winkle is a true historical story (it is a legend)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where did Rip Van Winkle live?',
        hint: 'Near a mountain range.',
        options: ['Himalayas', 'Kaatskill Mountains', 'Alps', 'Andes'],
        correctAnswer: 'Kaatskill Mountains',
        explanation: 'Rip lived in a village at the foot of the Kaatskill mountains.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Fred', back: 'The name of the lazy frog'),
      Flashcard(front: 'Companion', back: 'Rip\'s dog named Wolf')
    ],
    revisionNotes: 'Legends often involve magic or mysterious events. Laziness leads to missed life.',
    commonMistakes: ['Spelling of "Van Winkle"']
  ),

  'en5_c6': const ConceptNode(
    id: 'en5_c6',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 6: Class Discussion / The Talkative Barber',
    topic: 'Communication',
    subtopic: 'Discussion and Wit',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand how to participate in a discussion',
      'Identify traits of talkative vs quiet people',
      'Arabic folklore themes'
    ],
    examples: ['Jane being quiet in class', 'The Barber wasting Sultan\'s time'],
    misconceptions: ['Talking a lot means you are very wise'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why did the Sultan give all his food to the Barber?',
        hint: 'He wanted to get his head shaved quickly.',
        options: ['He was generous', 'To get rid of him', 'The food was bad', 'He was not hungry'],
        correctAnswer: 'To get rid of him',
        explanation: 'The Sultan was desperate for the Barber to stop talking and finish the work.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Discussion', back: 'Talking together in a group about a topic'),
      Flashcard(front: 'Defect', back: 'A fault or problem (The Barber called his brothers defective)')
    ],
    revisionNotes: 'Active listening is part of a good discussion. Arabian Nights is a collection of famous stories.',
    commonMistakes: ['Interrupting others during discussion']
  ),

  'en5_c7': const ConceptNode(
    id: 'en5_c7',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 7: Topsy-turvy Land / Gulliver’s Travels',
    topic: 'Imagination',
    subtopic: 'Fantasy and Scale',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Compare real world with imaginary Topsy-turvy land',
      'Understand the concept of relative size (Giants)',
      'Descriptive writing skills'
    ],
    examples: ['Walking on hands in Topsy-turvy land', 'Gulliver in Brobdingnag (Land of Giants)'],
    misconceptions: ['Gulliver only went to the land of small people (Lilliput)'],
    practiceExercises: [
      PracticeExercise(
        question: 'In Topsy-turvy land, where do the boats travel?',
        hint: 'It is the opposite of water.',
        options: ['In the sky', 'On the streets', 'In the sea', 'Underground'],
        correctAnswer: 'On the streets',
        explanation: 'In this imaginary land, boats travel on streets and you walk on your hands.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Brobdingnag', back: 'The land of Giants Gulliver visited'),
      Flashcard(front: 'Pleasure', back: 'A feeling of happy satisfaction')
    ],
    revisionNotes: 'Use adjectives like "enormous", "monstrous", "tiny" to describe scale.',
    commonMistakes: ['Confusing the sequence of Gulliver\'s voyages']
  ),

  'en5_c8': const ConceptNode(
    id: 'en5_c8',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 8: Nobody’s Friend / The Little Bully',
    topic: 'Social Skills',
    subtopic: 'Friendship and Empathy',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Identify behaviors that win or lose friends',
      'Impact of bullying on others',
      'Learning to share and be kind'
    ],
    examples: ['Hari pinching others', 'The girl who wouldn\'t share her sweets'],
    misconceptions: ['Bullying makes you look "cool" or strong'],
    practiceExercises: [
      PracticeExercise(
        question: 'What lesson did Hari learn at the seaside?',
        hint: 'The crabs pinched him.',
        options: ['How to swim', 'How it feels to be pinched', 'How to catch crabs', 'To eat more cake'],
        correctAnswer: 'How it feels to be pinched',
        explanation: 'After the crabs pinched him, Hari realized how much he hurt his classmates.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Sharing', back: 'A key to making friends'),
      Flashcard(front: 'Empathy', back: 'Understanding how someone else feels')
    ],
    revisionNotes: 'Be nice to others if you want them to be nice to you. Sharing is caring.',
    commonMistakes: ['Thinking being a bystander is okay']
  ),

  'en5_c9': const ConceptNode(
    id: 'en5_c9',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 9: Sing a Song of People / Around the World',
    topic: 'Geography and Culture',
    subtopic: 'Travel and Urban Life',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Contrast city life with quiet life',
      'Understand different modes of transport',
      'Adventure across continents (Phileas Fogg)'
    ],
    examples: ['Subways and elevators in cities', 'The train through the Rocky Mountains'],
    misconceptions: ['"Around the World in 80 Days" is a modern story (it was written in 1872)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who was the main character in "Around the World"?',
        hint: 'He made a bet to travel the world.',
        options: ['Robinson Crusoe', 'Phileas Fogg', 'Gulliver', 'Rip Van Winkle'],
        correctAnswer: 'Phileas Fogg',
        explanation: 'Phileas Fogg took the challenge to travel the world in exactly 80 days.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Subway', back: 'An underground electric railroad'),
      Flashcard(front: 'Rocky Mountains', back: 'Mountain range in North America')
    ],
    revisionNotes: 'The world is a large place with diverse people and landscapes.',
    commonMistakes: ['Spelling of "Phileas"']
  ),

  'en5_c10': const ConceptNode(
    id: 'en5_c10',
    subject: 'English',
    classLevel: 5,
    chapter: 'Unit 10: Malu Bhalu / Who Will be Ningthou?',
    topic: 'Leadership',
    subtopic: 'Bravery and Justice',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Qualities of a good leader (Justice, Empathy)',
      'Coming of age and learning skills (Malu the Polar Bear)',
      'Manipur folklore and culture'
    ],
    examples: ['Malu learning to swim', 'Sanatombi becoming the Meithel Leima'],
    misconceptions: ['A leader is only the strongest person'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why did the Ningthou choose Sanatombi as the future ruler?',
        hint: 'She felt the pain of nature.',
        options: ['She was eldest', 'She won a race', 'She was kind and empathetic', 'She was strong'],
        correctAnswer: 'She was kind and empathetic',
        explanation: 'The king chose her because she could feel the pain of people, animals, and trees.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Ningthou', back: 'The King (in Manipur)'),
      Flashcard(front: 'Malu Bhalu', back: 'A brave polar bear girl')
    ],
    revisionNotes: 'True leadership involves thinking about everyone\'s well-being.',
    commonMistakes: ['Confusing the three sons with the daughter\'s success']
  ),

  // ===========================================================================
  // CLASS 5 HINDI (Rimjhim)
  // ===========================================================================

  'h5_c1': const ConceptNode(
    id: 'h5_c1',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Raakh ki Rassi',
    topic: 'Literature',
    subtopic: 'Wisdom and Wit',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand Tibetan folklore',
      'Identify traits of wit and intelligence',
      'Learn Hindi vocabulary related to stories'
    ],
    examples: ['Lonpo Gar\'s son', 'The girl who made a rope of ash'],
    misconceptions: ['Thinking stories from other countries are not part of NCERT'],
    practiceExercises: [
      PracticeExercise(
        question: 'Lonpo Gar was a minister of which place?',
        hint: 'It is a place with high mountains.',
        options: ['India', 'Tibet', 'Nepal', 'China'],
        correctAnswer: 'Tibet',
        explanation: 'Lonpo Gar was the minister of Sonam Gampo, the King of Tibet.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Haazirjawabi', back: 'Wittiness / Quick in replying'),
      Flashcard(front: 'Bholapan', back: 'Innocence (trait of the son)')
    ],
    revisionNotes: 'Wit can solve problems that strength cannot.',
    commonMistakes: ['Spelling of Tibetan names in Hindi']
  ),

  'h5_c2': const ConceptNode(
    id: 'h5_c2',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Faslon ke Tyohar',
    topic: 'Culture',
    subtopic: 'Harvest Festivals of India',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about different harvest festivals across India',
      'Understand the cultural significance of crops',
      'Hindi names for regional festivals'
    ],
    examples: ['Makar Sankranti', 'Bihu', 'Pongal', 'Lohri'],
    misconceptions: ['All Indians celebrate the same festival in the same way'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which festival is celebrated in Assam to mark harvest?',
        hint: 'It involves dancing and music.',
        options: ['Pongal', 'Lohri', 'Bihu', 'Onam'],
        correctAnswer: 'Bihu',
        explanation: 'Bihu is the major harvest festival of Assam.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Khichdi', back: 'A festival name for Makar Sankranti in Bihar/UP'),
      Flashcard(front: 'Sohrai', back: 'Harvest festival of Adivasis in Jharkhand')
    ],
    revisionNotes: 'Festivals bring people together and celebrate nature\'s gifts.',
    commonMistakes: ['Confusing states with their specific festivals']
  ),

  'h5_c3': const ConceptNode(
    id: 'h5_c3',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Khilaunewala',
    topic: 'Poetry',
    subtopic: 'Imagination and Childhood',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.create,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Enjoy the rhythm of Hindi poetry',
      'Learn names of toys and mythological characters',
      'Express desire through verse'
    ],
    examples: ['Ramayana references (Ram, Kaushalya)', 'Toy motor-cars and whistles'],
    misconceptions: ['The poem is only about buying toys'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who wrote the poem "Khilaunewala"?',
        hint: 'She is a famous Hindi poetess.',
        options: ['Mahadevi Verma', 'Subhadra Kumari Chauhan', 'Nirmala Deshpande', 'Sarojini Naidu'],
        correctAnswer: 'Subhadra Kumari Chauhan',
        explanation: 'The poem was composed by Subhadra Kumari Chauhan.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Talwar', back: 'Sword'),
      Flashcard(front: 'Teer-kaman', back: 'Bow and arrow')
    ],
    revisionNotes: 'The child wants to be like Ram and kill demons like Tadka.',
    commonMistakes: ['Identifying the poet correctly']
  ),

  'h5_c4': const ConceptNode(
    id: 'h5_c4',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Nanha Fankar',
    topic: 'Art and History',
    subtopic: 'Sculpture and Akbar',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about stone carving (sculpture)',
      'Life at the time of Emperor Akbar',
      'Passion for craft at a young age'
    ],
    examples: ['Keshav (the young artist)', 'Fatehpur Sikri construction'],
    misconceptions: ['Kings were always scary and unapproachable'],
    practiceExercises: [
      PracticeExercise(
        question: 'What was the age of Keshav?',
        hint: 'He was a young boy.',
        options: ['10 years', '12 years', '15 years', '8 years'],
        correctAnswer: '10 years',
        explanation: 'Keshav was a 10-year-old boy who was learning stone carving.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Fankar', back: 'Artist / Craftsman'),
      Flashcard(front: 'Chaini-Hathauda', back: 'Chisel and Hammer')
    ],
    revisionNotes: 'Hard work and talent are respected even by Kings.',
    commonMistakes: ['Spelling of "Fatehpur Sikri"']
  ),

  'h5_c5': const ConceptNode(
    id: 'h5_c5',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Jahan Chah Wahan Raah',
    topic: 'Biography',
    subtopic: 'Determination and Skill',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Inspirational story of Ila Sachani',
      'Overcoming physical disability',
      'Traditional embroidery styles'
    ],
    examples: ['Kasuti embroidery', 'Kashmiri work', 'Using feet for sewing'],
    misconceptions: ['Disabled people cannot do intricate handwork'],
    practiceExercises: [
      PracticeExercise(
        question: 'Ila Sachani was an expert in which craft?',
        hint: 'It involves needle and thread.',
        options: ['Pottery', 'Embroidery', 'Painting', 'Cooking'],
        correctAnswer: 'Embroidery',
        explanation: 'Despite having disabled hands, she learned to embroider with her feet.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Zardozi', back: 'A type of heavy and elaborate metal embroidery'),
      Flashcard(front: 'Ila\'s state', back: 'Gujarat')
    ],
    revisionNotes: 'Willpower can turn impossible into possible.',
    commonMistakes: ['Thinking she used her hands for embroidery']
  ),

  'h5_c6': const ConceptNode(
    id: 'h5_c6',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Chitthi ka Safar',
    topic: 'Communication',
    subtopic: 'History of Postal System',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.remember,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Evolution of letters and messages',
      'Function of PIN codes',
      'Use of pigeons in ancient times'
    ],
    examples: ['Harkara (messengers)', 'Speed post', 'Email vs Letter'],
    misconceptions: ['PIN code is just a random number'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the full form of PIN in PIN Code?',
        hint: 'It relates to the post office.',
        options: ['Personal Id Number', 'Postal Index Number', 'Public Info Net', 'Private Int Node'],
        correctAnswer: 'Postal Index Number',
        explanation: 'PIN stands for Postal Index Number, used to sort mail easily.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Pigeon post', back: 'Using Homa pigeons to carry messages'),
      Flashcard(front: 'PIN digits', back: '6 digits in India')
    ],
    revisionNotes: 'Addresses must be complete with name, house number, area, and PIN.',
    commonMistakes: ['Writing wrong PIN codes']
  ),

  'h5_c7': const ConceptNode(
    id: 'h5_c7',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Dakiy ki Bhent',
    topic: 'Interview',
    subtopic: 'Life of a Public Servant',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 3,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the format of an interview',
      'Life challenges of a postman in hilly areas',
      'Value of a postman in remote villages'
    ],
    examples: ['Kunwar Singh (the postman)', 'Shimla district challenges'],
    misconceptions: ['Postmen only deliver letters in cities'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who was interviewed in this chapter?',
        hint: 'He is a postman.',
        options: ['Keshav', 'Lonpo Gar', 'Kunwar Singh', 'Bishan'],
        correctAnswer: 'Kunwar Singh',
        explanation: 'Kunwar Singh from Shimla district shares his experience as a postman.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Interview', back: 'A conversation where questions are asked and answered'),
      Flashcard(front: 'Packer', back: 'A post office staff member who packs mail')
    ],
    revisionNotes: 'Postmen are trusted messengers in villages, carrying pensions and money orders.',
    commonMistakes: ['Missing the interview context']
  ),

  'h5_c8': const ConceptNode(
    id: 'h5_c8',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Ve Din bhi kya Din the',
    topic: 'Science Fiction',
    subtopic: 'Future of Education',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Contrast traditional books with screen-based reading',
      'Imagining a school with mechanical teachers',
      'Value of social interaction in schools'
    ],
    examples: ['Tommy and Kummi', 'Finding a real paper book'],
    misconceptions: ['Mechanical teachers are better than human teachers'],
    practiceExercises: [
      PracticeExercise(
        question: 'In the future story, where did students study?',
        hint: 'It was inside their own house.',
        options: ['A big building', 'A park', 'A room in their house', 'A library'],
        correctAnswer: 'A room in their house',
        explanation: 'The story imagines students having a mechanical teacher in a room at home.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Mechanical Teacher', back: 'A robot or computer that teaches'),
      Flashcard(front: 'Real Book', back: 'A book made of paper with printed words')
    ],
    revisionNotes: 'Traditional schools allow children to play and learn together.',
    commonMistakes: ['Confusing the past with the future setting of the story']
  ),

  'h5_c9': const ConceptNode(
    id: 'h5_c9',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Ek Maa ki Bebasi',
    topic: 'Poetry',
    subtopic: 'Empathy and Inclusion',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the feelings of a non-verbal child',
      'Learn to empathize with people who are different',
      'Express helplessness through poetry'
    ],
    examples: ['Ratan (the child)', 'Mother\'s constant gaze'],
    misconceptions: ['People who cannot speak do not have thoughts or feelings'],
    practiceExercises: [
      PracticeExercise(
        question: 'How did Ratan communicate with other children?',
        hint: 'He used his eyes and hands.',
        options: ['By writing', 'By signs/gestures', 'By singing', 'By shouting'],
        correctAnswer: 'By signs/gestures',
        explanation: 'Ratan was unable to speak, so he used gestures and expressions to communicate.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Bebasi', back: 'Helplessness'),
      Flashcard(front: 'Poet', back: 'Kunwar Narain')
    ],
    revisionNotes: 'Everyone deserves friends, even if they communicate differently.',
    commonMistakes: ['Ignoring the emotional depth of the poem']
  ),

  'h5_c10': const ConceptNode(
    id: 'h5_c10',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Ek Din ki Badshahat',
    topic: 'Drama',
    subtopic: 'Roles and Freedom',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.create,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand children\'s desire for freedom',
      'Learn about role-reversal in a family',
      'Hindi synonyms for power and rules'
    ],
    examples: ['Arif and Salim', 'Giving orders to elders'],
    misconceptions: ['The story is about becoming a real king'],
    practiceExercises: [
      PracticeExercise(
        question: 'What did Arif and Salim want from their father (Abba)?',
        hint: 'They wanted to be in charge for a day.',
        options: ['New clothes', 'One day of power', 'Money', 'Vacation'],
        correctAnswer: 'One day of power',
        explanation: 'They wanted to treat the elders the way elders treated them for one day.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Badshahat', back: 'Kingship / Sovereignty'),
      Flashcard(front: 'Pabandi', back: 'Restriction / Ban')
    ],
    revisionNotes: 'Empathy grows when we experience life from another person\'s perspective.',
    commonMistakes: ['Missing the humour in the boys\' actions']
  ),

  'h5_c11': const ConceptNode(
    id: 'h5_c11',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Chawal ki Rotiyan',
    topic: 'Drama',
    subtopic: 'Wit and Excuses',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 3,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about Burmese culture and setting',
      'Follow the consequences of lying/making excuses',
      'Dialogue delivery in a play'
    ],
    examples: ['Koko hiding his rice cakes', 'Friends visiting unexpectedly'],
    misconceptions: ['Koko was a mean person (he was just hungry and protective)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why did Koko hide the rice cakes?',
        hint: 'He didn\'t want to share.',
        options: ['They were poisoned', 'They were stale', 'He wanted to eat them all', 'They were for his sister'],
        correctAnswer: 'He wanted to eat them all',
        explanation: 'Koko loved rice cakes and didn\'t want to share them with his friends.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Chawal ki Rotiyan', back: 'Rice cakes / Breads'),
      Flashcard(front: 'Bahana', back: 'Excuse')
    ],
    revisionNotes: 'Sharing with friends makes the food taste better and keeps the heart light.',
    commonMistakes: ['Thinking the play is set in India']
  ),

  'h5_c12': const ConceptNode(
    id: 'h5_c12',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Guru aur Chela',
    topic: 'Poetry',
    subtopic: 'Foolishness and Justice',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Humorous take on a foolish kingdom (Andher Nagari)',
      'Rhyme scheme and flow of the poem',
      'Moral lesson on logic and justice'
    ],
    examples: ['Everything costing one "Taka"', 'The wall falling and looking for a culprit'],
    misconceptions: ['The Guru was selfish for leaving the Chela'],
    practiceExercises: [
      PracticeExercise(
        question: 'What was the name of the kingdom in the poem?',
        hint: 'It was a dark/foolish place.',
        options: ['Sunder Nagari', 'Andher Nagari', 'Ujala Nagari', 'Lal Nagari'],
        correctAnswer: 'Andher Nagari',
        explanation: 'Andher Nagari was a kingdom where the king was foolish and rules were non-existent.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Andher Nagari', back: 'Kingdom of Chaos'),
      Flashcard(front: 'Taka', back: 'A small unit of currency')
    ],
    revisionNotes: 'A wise person stays away from places where there is no logic or justice.',
    commonMistakes: ['Confusing the Chela\'s greed with wisdom']
  ),

  'h5_c13': const ConceptNode(
    id: 'h5_c13',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Swami ki Dadi',
    topic: 'Literature',
    subtopic: 'Grandparents and Stories',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Relationship between grandchild and grandparent',
      'R.K. Narayan\'s storytelling style (Malgudi context)',
      'Handling pride and boasting'
    ],
    examples: ['Swami telling Dadi about Rajam', 'Dadi\'s old stories of Grandfather'],
    misconceptions: ['Dadi was ignoring Swami (she was just old and sleepy)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who was the hero of Swami\'s stories?',
        hint: 'He was a brave boy with a gun.',
        options: ['Mani', 'Rajam', 'Sankar', 'The Postman'],
        correctAnswer: 'Rajam',
        explanation: 'Swami was very proud of his friend Rajam and told many stories about him to Dadi.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Swami\'s real name', back: 'Swaminathan'),
      Flashcard(front: 'Boasting', back: 'Shekhi baghaarna')
    ],
    revisionNotes: 'Listening to elders\' stories connects us to our family history.',
    commonMistakes: ['Thinking the story is set in a modern city']
  ),

  'h5_c14': const ConceptNode(
    id: 'h5_c14',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Baagh aaya us Raat',
    topic: 'Poetry',
    subtopic: 'Fear and Nature',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the perspective of a child about danger',
      'Learn about the habitat of tigers',
      'Conversational style in Hindi poetry'
    ],
    examples: ['Tiger living in a cave', 'Child warning Baba not to go out at night'],
    misconceptions: ['Tigers only come to villages to hurt people'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is warning the elders about the tiger?',
        hint: 'He is a young child.',
        options: ['The King', 'The Postman', 'The 5-year-old child', 'The Hunter'],
        correctAnswer: 'The 5-year-old child',
        explanation: 'The poem is a conversation where a child is telling his father about a tiger sighting.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Baba', back: 'Father / Grandfather'),
      Flashcard(front: 'Sachet', back: 'Alert / Careful')
    ],
    revisionNotes: 'Wildlife often overlaps with human habitats in some areas. Caution is key.',
    commonMistakes: ['Thinking the tiger actually entered the house']
  ),

  'h5_c15': const ConceptNode(
    id: 'h5_c15',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Bishan ki Dileri',
    topic: 'Story',
    subtopic: 'Bravery and Compassion',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Moral value of protecting animals',
      'Challenges of living in hilly areas',
      'Heroism shown by a young boy'
    ],
    examples: ['Bishan saving a wounded Pheasant (Teetar)', 'Hiding from the hunters'],
    misconceptions: ['Hunting is always a "sport" (it is often cruel/illegal)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which bird did Bishan save?',
        hint: 'It is a small game bird.',
        options: ['Peacock', 'Pheasant (Teetar)', 'Pigeon', 'Parrot'],
        correctAnswer: 'Pheasant (Teetar)',
        explanation: 'Bishan risked his safety to save a pheasant that was wounded by hunters.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Dileri', back: 'Bravery / Courage'),
      Flashcard(front: 'Khet', back: 'Fields (Step fields in hills)')
    ],
    revisionNotes: 'Compassion for living beings is the highest form of bravery.',
    commonMistakes: ['Spelling of "Teetar" in Hindi']
  ),

  'h5_c16': const ConceptNode(
    id: 'h5_c16',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Pani re Pani',
    topic: 'Environment',
    subtopic: 'Water Cycle and Crisis',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['e5_c6'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the source of water in our taps',
      'Learn about water shortage and its causes',
      'Importance of preserving ponds and lakes'
    ],
    examples: ['Groundwater levels', 'Encroachment on old ponds'],
    misconceptions: ['Water comes only from the tap (it comes from rivers/ground)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why are our groundwater levels going down?',
        hint: 'We are covering the soil and losing ponds.',
        options: ['Less rain', 'More people', 'Loss of ponds and concrete roads', 'Magic'],
        correctAnswer: 'Loss of ponds and concrete roads',
        explanation: 'When we fill up ponds and cover soil with concrete, rain water cannot go into the ground.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Jal Chakra', back: 'Water Cycle'),
      Flashcard(front: 'Bhu-jal', back: 'Groundwater')
    ],
    revisionNotes: 'Save every drop. Revive traditional water bodies.',
    commonMistakes: ['Thinking rain is the only solution for water crisis']
  ),

  'h5_c17': const ConceptNode(
    id: 'h5_c17',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Chhoti si Hamari Nadi',
    topic: 'Poetry',
    subtopic: 'Nature and Seasons',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Appreciate the beauty of a river in different seasons',
      'Identify onomatopoeic words (words that sound like what they mean)',
      'Tagore\'s poetic style'
    ],
    examples: ['Kans flowers', 'Chik-chik of Mainas', 'Kich-pich sounds'],
    misconceptions: ['Rivers are the same all year round (they change in summer/monsoon)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who wrote the poem "Chhoti si Hamari Nadi"?',
        hint: 'He is India\'s first Nobel Laureate.',
        options: ['Premchand', 'Rabindranath Tagore', 'Nirala', 'Pant'],
        correctAnswer: 'Rabindranath Tagore',
        explanation: 'The poem was originally written by Rabindranath Tagore.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Dhaar', back: 'Flow / Current'),
      Flashcard(front: 'Ghamasaan', back: 'Very intense / Heavy (rain)')
    ],
    revisionNotes: 'Summer: River is shallow. Monsoon: River is full and fast.',
    commonMistakes: ['Misidentifying the poet']
  ),

  'h5_c18': const ConceptNode(
    id: 'h5_c18',
    subject: 'Hindi',
    classLevel: 5,
    chapter: 'Chunauti Himalay ki',
    topic: 'Adventure',
    subtopic: 'Mountaineering and Spirit',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: ['e5_c9'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Story of Jawaharlal Nehru\'s trek to Amarnath',
      'Challenges of breathing and trekking in high altitude',
      'Awe and respect for the Himalayas'
    ],
    examples: ['Zojila pass', 'Mataun pass', 'Crevasses hidden in snow'],
    misconceptions: ['Nehru only did politics (he was also an adventurer)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where was Nehru trying to reach in this story?',
        hint: 'A holy cave in the Himalayas.',
        options: ['Kedarnath', 'Amarnath', 'Badrinath', 'Gangotri'],
        correctAnswer: 'Amarnath',
        explanation: 'Nehru was on a trek from Zojila to reach the Amarnath cave.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Chunauti', back: 'Challenge'),
      Flashcard(front: 'Him-shikhar', back: 'Snow peaks')
    ],
    revisionNotes: 'Himalayas are beautiful but require great caution and preparation to climb.',
    commonMistakes: ['Thinking he reached the destination (he had to return due to bad weather/cracks)']
  ),

  // ===========================================================================
  // CLASS 6 MATHEMATICS
  // ===========================================================================

  'm6_c1': const ConceptNode(
    id: 'm6_c1',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Knowing Our Numbers',
    topic: 'Number System',
    subtopic: 'Large Numbers and Estimation',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['m5_c1'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Compare large numbers effectively',
      'Use Indian and International place value systems',
      'Understand Estimation and Roman Numerals'
    ],
    examples: ['1 million = 10 lakhs', 'Estimation of 4875 to nearest thousand is 5000'],
    misconceptions: ['Thinking Roman numerals have a symbol for zero (they do not)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Insert commas in International system: 987654321',
        hint: 'Use groups of 3.',
        options: ['98,76,54,321', '987,654,321', '9,8,7,6,5,4,3,2,1', '9876,54321'],
        correctAnswer: '987,654,321',
        explanation: 'International system uses 3-digit groupings: Millions, Thousands, Ones.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Roman Numeral L', back: '50'),
      Flashcard(front: 'Roman Numeral C', back: '100'),
      Flashcard(front: 'Roman Numeral D', back: '500'),
      Flashcard(front: 'Roman Numeral M', back: '1000')
    ],
    revisionNotes: 'Estimation makes big calculations easier and faster. Roman numerals follow addition/subtraction rules.',
    commonMistakes: ['Writing IVVV for 15 (cannot repeat V)']
  ),

  'm6_c2': const ConceptNode(
    id: 'm6_c2',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Whole Numbers',
    topic: 'Number System',
    subtopic: 'Properties and Patterns',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['m5_c1'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Difference between Natural and Whole numbers',
      'Representation on number line',
      'Commutative, Associative, and Distributive properties'
    ],
    examples: ['a + b = b + a (Commutative)', '0 is the additive identity'],
    misconceptions: ['Division by zero is zero (it is undefined)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the successor of 0?',
        hint: 'Add 1 to the number.',
        options: ['-1', '0', '1', 'None'],
        correctAnswer: '1',
        explanation: '0 + 1 = 1.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Natural Numbers', back: 'Counting numbers 1, 2, 3...'),
      Flashcard(front: 'Whole Numbers', back: 'Natural numbers including 0')
    ],
    revisionNotes: 'Property of Distributivity: a * (b + c) = (a * b) + (a * c).',
    commonMistakes: ['Applying commutative property to subtraction']
  ),

  'm6_c3': const ConceptNode(
    id: 'm6_c3',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Playing with Numbers',
    topic: 'Number Theory',
    subtopic: 'LCM, HCF and Divisibility',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.apply,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 60),
    prerequisites: ['m5_c6'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Apply divisibility tests (2 to 11)',
      'Find prime and composite numbers (Eratosthenes Sieve)',
      'Calculate HCF and LCM of multiple numbers'
    ],
    examples: ['Number is divisible by 3 if sum of digits is divisible by 3', '2 is the only even prime'],
    misconceptions: ['1 is a prime number (it is neither prime nor composite)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the HCF of 15 and 20?',
        hint: 'Find the largest number that divides both.',
        options: ['60', '1', '5', '10'],
        correctAnswer: '5',
        explanation: 'Factors of 15: 1, 3, 5, 15. Factors of 20: 1, 2, 4, 5, 10, 20. Largest common is 5.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Perfect Number', back: 'Sum of its factors equals twice the number (e.g., 6)'),
      Flashcard(front: 'Co-prime', back: 'Two numbers having only 1 as common factor')
    ],
    revisionNotes: 'If a number is divisible by 9, it is also divisible by 3.',
    commonMistakes: ['Confusing LCM calculation with HCF']
  ),

  'm6_c4': const ConceptNode(
    id: 'm6_c4',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Basic Geometrical Ideas',
    topic: 'Geometry',
    subtopic: 'Points, Lines and Curves',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.remember,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: ['m5_c2'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Define point, line, ray, and line segment',
      'Distinguish between open and closed curves',
      'Parts of a polygon and circle'
    ],
    examples: ['Diameter is twice the radius', 'A triangle is a 3-sided polygon'],
    misconceptions: ['A ray is same as a line (ray has one end point, line has zero)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which of these has infinite length and no end points?',
        hint: 'It goes on forever in both directions.',
        options: ['Ray', 'Line Segment', 'Line', 'Point'],
        correctAnswer: 'Line',
        explanation: 'A line has no ends and extends infinitely.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Chord', back: 'Line segment joining two points on a circle'),
      Flashcard(front: 'Sector', back: 'Region bounded by an arc and two radii')
    ],
    revisionNotes: 'Geometry comes from "Geo" (Earth) and "Metron" (Measurement).',
    commonMistakes: ['Confusing Sector with Segment in a circle']
  ),

  'm6_c5': const ConceptNode(
    id: 'm6_c5',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Understanding Elementary Shapes',
    topic: 'Geometry',
    subtopic: 'Angles, Triangles and 3D',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: ['m5_c2', 'm5_c9'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Measure angles using a protractor',
      'Classify triangles by sides and angles',
      'Identify types of quadrilaterals (Parallelogram, Rhombus, etc.)'
    ],
    examples: ['Equilateral triangle has 3 equal sides', 'Protractor for measuring degrees'],
    misconceptions: ['Thinking every rectangle is a square (every square is a rectangle)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What do you call a triangle with two equal sides?',
        hint: 'It starts with I.',
        options: ['Scalene', 'Equilateral', 'Isosceles', 'Right-angled'],
        correctAnswer: 'Isosceles',
        explanation: 'Isosceles triangles have two sides of the same length.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Reflex Angle', back: 'Greater than 180 and less than 360'),
      Flashcard(front: 'Prism', back: '3D shape with same base and top')
    ],
    revisionNotes: 'Clock directions: 1/4 turn = 90 deg, 1/2 turn = 180 deg.',
    commonMistakes: ['Misreading the scale of a protractor']
  ),

  'm6_c6': const ConceptNode(
    id: 'm6_c6',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Integers',
    topic: 'Number System',
    subtopic: 'Negative Numbers',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['m6_c2'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the need for negative numbers',
      'Compare integers on a number line',
      'Perform addition and subtraction of integers'
    ],
    examples: ['Temperature below zero', 'Spending money as a negative value'],
    misconceptions: ['Thinking -10 is bigger than -2 (actually -2 is closer to zero, so it\'s bigger)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is -5 + 8?',
        hint: 'Start at -5 on number line and move 8 steps right.',
        options: ['13', '-13', '3', '-3'],
        correctAnswer: '3',
        explanation: '-5 + 8 = 3.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Integer', back: 'Whole numbers and their negatives'),
      Flashcard(front: 'Zero', back: 'Neither positive nor negative')
    ],
    revisionNotes: 'Subtracting a negative number is like adding its positive counterpart.',
    commonMistakes: ['Signs errors during addition/subtraction']
  ),

  'm6_c7': const ConceptNode(
    id: 'm6_c7',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Fractions',
    topic: 'Number System',
    subtopic: 'Types and Operations',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: ['m5_c4'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Proper, Improper, and Mixed fractions',
      'Simplifying fractions to lowest terms',
      'Adding and subtracting like and unlike fractions'
    ],
    examples: ['3/2 is an improper fraction (1 1/2 as mixed)', '1/2 + 1/4 = 3/4'],
    misconceptions: ['You can add numerators even if denominators are different'],
    practiceExercises: [
      PracticeExercise(
        question: 'Reduce to simplest form: 12/18',
        hint: 'Divide both by their HCF (6).',
        options: ['2/3', '3/2', '6/9', '4/6'],
        correctAnswer: '2/3',
        explanation: '12/6 = 2, 18/6 = 3. So 2/3.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Proper Fraction', back: 'Numerator < Denominator'),
      Flashcard(front: 'Like Fractions', back: 'Fractions with same denominator')
    ],
    revisionNotes: 'Find LCM of denominators to add unlike fractions.',
    commonMistakes: ['Forgetting to find common denominator']
  ),

  'm6_c8': const ConceptNode(
    id: 'm6_c8',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Decimals',
    topic: 'Number System',
    subtopic: 'Expansion of Tenths and Hundredths',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['m5_c10'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Represent decimals on number line',
      'Compare decimals like 0.07 and 0.1',
      'Add and subtract decimal numbers'
    ],
    examples: ['0.5 = 5/10', '0.07 < 0.1 because 0.07 < 0.10'],
    misconceptions: ['Adding 1.2 and 0.03 as 0.15 (should be 1.23)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Write 4 tens and 2 tenths as a decimal.',
        hint: '40 + 2/10.',
        options: ['4.2', '42.0', '40.2', '0.42'],
        correctAnswer: '40.2',
        explanation: '4 tens = 40. 2 tenths = 0.2. Total = 40.2.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Decimals in Money', back: '100 paise = 1 rupee'),
      Flashcard(front: 'Decimals in Weight', back: '1000g = 1kg')
    ],
    revisionNotes: 'Align decimal points vertically when adding or subtracting.',
    commonMistakes: ['Misaligning digits during addition']
  ),

  'm6_c9': const ConceptNode(
    id: 'm6_c9',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Data Handling',
    topic: 'Data Handling',
    subtopic: 'Pictographs and Bar Graphs',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['m5_c12'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Record data using tally marks',
      'Construct and interpret Pictographs',
      'Draw Bar Graphs for discrete data'
    ],
    examples: ['One symbol = 10 students in a pictograph', 'Scale of 1 unit = 100 people in bar graph'],
    misconceptions: ['Pictographs are just for fun and not accurate'],
    practiceExercises: [
      PracticeExercise(
        question: 'If a star symbol in a pictograph represents 5 children, how many stars represent 20 children?',
        hint: 'Divide 20 by 5.',
        options: ['2', '3', '4', '5'],
        correctAnswer: '4',
        explanation: '20 / 5 = 4 symbols.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Pictograph', back: 'Representing data through pictures of objects'),
      Flashcard(front: 'Bar Graph', back: 'Representing data using bars of uniform width')
    ],
    revisionNotes: 'Scale selection is critical for a clear graph.',
    commonMistakes: ['Uneven width of bars in a bar graph']
  ),

  'm6_c10': const ConceptNode(
    id: 'm6_c10',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Mensuration',
    topic: 'Measurement',
    subtopic: 'Area and Perimeter Formulas',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['m5_c11'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Find perimeter of regular polygons using formulas',
      'Calculate area of rectangle and square',
      'Solve daily life problems involving fencing and tiling'
    ],
    examples: ['Perimeter of hexagon = 6 * side', 'Area of square = side * side'],
    misconceptions: ['Thinking area and perimeter are the same thing'],
    practiceExercises: [
      PracticeExercise(
        question: 'Find perimeter of equilateral triangle with side 5cm.',
        hint: '3 * side.',
        options: ['10 cm', '15 cm', '25 cm', '5 cm'],
        correctAnswer: '15 cm',
        explanation: '3 * 5 = 15cm.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Perimeter of Rectangle', back: '2 * (Length + Breadth)'),
      Flashcard(front: 'Area of Rectangle', back: 'Length * Breadth')
    ],
    revisionNotes: 'Perimeter is length of boundary. Area is surface covered.',
    commonMistakes: ['Calculation errors in addition/multiplication']
  ),

  'm6_c11': const ConceptNode(
    id: 'm6_c11',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Algebra',
    topic: 'Algebra',
    subtopic: 'Introduction to Variables',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: ['m5_c7'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand variables as letters replacing numbers',
      'Translate simple statements into algebraic expressions',
      'Introduction to equations and solutions'
    ],
    examples: ['Matchstick patterns: 2n for number of matchsticks', 'x + 5 = 12'],
    misconceptions: ['Thinking a variable has a fixed value always (it varies!)'],
    practiceExercises: [
      PracticeExercise(
        question: 'If "x" represents age now, what is age 5 years ago?',
        hint: 'Go back in time.',
        options: ['x + 5', '5x', 'x - 5', 'x / 5'],
        correctAnswer: 'x - 5',
        explanation: '5 years ago means subtraction: x - 5.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Variable', back: 'A letter that can take various numerical values'),
      Flashcard(front: 'Equation', back: 'Condition on a variable with an equality sign')
    ],
    revisionNotes: 'Algebra helps us solve problems by generalizing rules.',
    commonMistakes: ['Confusing 2x with x + 2']
  ),

  'm6_c12': const ConceptNode(
    id: 'm6_c12',
    subject: 'Mathematics',
    classLevel: 6,
    chapter: 'Ratio and Proportion',
    topic: 'Arithmetic',
    subtopic: 'Comparison and Unitary Method',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: ['m6_c7'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Compare quantities using ratios',
      'Check if two ratios are in proportion',
      'Apply Unitary Method to solve problems'
    ],
    examples: ['Ratio of boys to girls 3:4', 'If 6 cans cost 210, cost of 4 cans is?'],
    misconceptions: ['Comparing values with different units directly (must convert first)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Are 15, 45, 40, 120 in proportion?',
        hint: 'Check if 15/45 = 40/120.',
        options: ['Yes', 'No'],
        correctAnswer: 'Yes',
        explanation: '15/45 = 1/3 and 40/120 = 1/3. They are equal.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Ratio', back: 'Comparison of two quantities by division'),
      Flashcard(front: 'Unitary Method', back: 'Finding value of one unit then many')
    ],
    revisionNotes: 'Ratios have no units.',
    commonMistakes: ['Changing the order of terms in a ratio']
  ),

  // ===========================================================================
  // CLASS 6 SCIENCE
  // ===========================================================================

  's6_c1': const ConceptNode(
    id: 's6_c1',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Components of Food',
    topic: 'Biology',
    subtopic: 'Nutrients and Balance',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.remember,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['e5_c3'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Identify nutrients: Carbohydrates, Proteins, Fats, Vitamins, Minerals',
      'Test for starch, protein, and fats',
      'Understand Balanced Diet and Deficiency diseases'
    ],
    examples: ['Iodine test for starch', 'Vitamin C prevents Scurvy'],
    misconceptions: ['Fats are always bad (essential for energy)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which nutrient is known as "body building" food?',
        hint: 'It helps in growth.',
        options: ['Carbohydrates', 'Proteins', 'Vitamins', 'Fats'],
        correctAnswer: 'Proteins',
        explanation: 'Proteins are needed for the growth and repair of our body.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Roughage', back: 'Dietary fibres that help in digestion'),
      Flashcard(front: 'Scurvy', back: 'Deficiency of Vitamin C')
    ],
    revisionNotes: 'Carbohydrates and fats provide energy. Proteins are for growth.',
    commonMistakes: ['Thinking water is a nutrient (it is essential but not a nutrient)']
  ),

  's6_c2': const ConceptNode(
    id: 's6_c2',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Sorting Materials into Groups',
    topic: 'Chemistry',
    subtopic: 'Properties of Materials',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: ['e5_c7'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Classify objects based on lustre, hardness, and transparency',
      'Understand solubility and density (floating/sinking)',
      'Purpose of grouping materials'
    ],
    examples: ['Glass is transparent', 'Wood is opaque', 'Salt is soluble'],
    misconceptions: ['All metals are hard (Sodium is soft)'],
    practiceExercises: [
      PracticeExercise(
        question: 'A material through which you can see clearly is?',
        hint: 'Like window glass.',
        options: ['Opaque', 'Translucent', 'Transparent', 'Hard'],
        correctAnswer: 'Transparent',
        explanation: 'Transparent materials allow light to pass through completely.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Lustre', back: 'Shine on the surface of materials'),
      Flashcard(front: 'Translucent', back: 'Allows light to pass partially')
    ],
    revisionNotes: 'Grouping helps in identifying and studying properties of materials.',
    commonMistakes: ['Confusing translucent with transparent']
  ),

  's6_c3': const ConceptNode(
    id: 's6_c3',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Separation of Substances',
    topic: 'Chemistry',
    subtopic: 'Methods of Separation',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn Handpicking, Winnowing, and Sieving',
      'Understand Sedimentation, Decantation, and Filtration',
      'Process of Evaporation and Condensation'
    ],
    examples: ['Separating tea leaves', 'Getting salt from sea water'],
    misconceptions: ['Filtration can remove dissolved salt (only evaporation can)'],
    practiceExercises: [
      PracticeExercise(
        question: 'The process of conversion of water vapour into its liquid form is?',
        hint: 'Opposite of evaporation.',
        options: ['Sedimentation', 'Condensation', 'Filtration', 'Winnowing'],
        correctAnswer: 'Condensation',
        explanation: 'Condensation is how clouds turn into rain.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Winnowing', back: 'Separating heavier and lighter components by wind'),
      Flashcard(front: 'Saturated Solution', back: 'No more solute can be dissolved at that temperature')
    ],
    revisionNotes: 'More than one method may be needed to separate a mixture.',
    commonMistakes: ['Confusing decantation with sedimentation']
  ),

  's6_c4': const ConceptNode(
    id: 's6_c4',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Getting to Know Plants',
    topic: 'Botany',
    subtopic: 'Plant Parts and Functions',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['e5_c5'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Classify: Herbs, Shrubs, Trees, Creepers, Climbers',
      'Functions of Stem, Leaf (Venation), and Root (Tap/Fibrous)',
      'Parts of a Flower (Sepals, Petals, Stamens, Pistil)'
    ],
    examples: ['Parallel venation in grass', 'Reticulate venation in peepal'],
    misconceptions: ['Plants only get food from soil (they make it via photosynthesis)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which part of the plant is responsible for Transpiration?',
        hint: 'It happens through stomata.',
        options: ['Stem', 'Root', 'Leaf', 'Flower'],
        correctAnswer: 'Leaf',
        explanation: 'Water comes out of leaves in the form of vapour by transpiration.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Pistil', back: 'Innermost part of a flower (Female)'),
      Flashcard(front: 'Tap Root', back: 'Main root with smaller lateral roots')
    ],
    revisionNotes: 'Plants are the primary producers. Leaves are the "kitchen" of the plant.',
    commonMistakes: ['Confusing Stamens with Pistils']
  ),

  's6_c5': const ConceptNode(
    id: 's6_c5',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Body Movements',
    topic: 'Biology',
    subtopic: 'Skeleton and Joints',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: ['e5_c1'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Types of joints: Ball and Socket, Pivotal, Hinge, Fixed',
      'Understand the human skeleton and X-rays',
      'Gait of animals (Earthworm, Snail, Cockroach, Fish, Bird)'
    ],
    examples: ['Shoulder joint (Ball and socket)', 'Knee joint (Hinge)'],
    misconceptions: ['Bones are not living (they are living tissues)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which joint allows movement in all directions?',
        hint: 'Think of your shoulder.',
        options: ['Hinge joint', 'Fixed joint', 'Ball and socket joint', 'Pivotal joint'],
        correctAnswer: 'Ball and socket joint',
        explanation: 'It allows the maximum range of motion.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Cartilage', back: 'Soft parts of skeleton (e.g. ear lobe)'),
      Flashcard(front: 'Rib Cage', back: 'Protects the heart and lungs')
    ],
    revisionNotes: 'Muscles work in pairs - one contracts while the other relaxes.',
    commonMistakes: ['Thinking snakes have no bones (they have a long backbone)']
  ),

  's6_c6': const ConceptNode(
    id: 's6_c6',
    subject: 'Science',
    classLevel: 6,
    chapter: 'The Living Organisms — Characteristics and Habitats',
    topic: 'Biology',
    subtopic: 'Adaptation and Environment',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Biotic and Abiotic components',
      'Adaptations in Desert, Mountain, and Marine habitats',
      'Common characteristics of living beings'
    ],
    examples: ['Cactus has spines for leaves', 'Snow leopards have thick fur'],
    misconceptions: ['Acclimatization is same as Adaptation (acclimatization is short-term)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which of these is an abiotic component?',
        hint: 'It is a non-living thing.',
        options: ['Plants', 'Animals', 'Soil', 'Bacteria'],
        correctAnswer: 'Soil',
        explanation: 'Abiotic components include non-living things like rocks, soil, air, and water.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Adaptation', back: 'Presence of specific features to live in a habitat'),
      Flashcard(front: 'Excretion', back: 'Getting rid of waste by living organisms')
    ],
    revisionNotes: 'Living things respond to stimuli, grow, and reproduce.',
    commonMistakes: ['Thinking all aquatic animals have gills (Dolphins/Whales have blowholes)']
  ),

  's6_c7': const ConceptNode(
    id: 's6_c7',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Motion and Measurement of Distances',
    topic: 'Physics',
    subtopic: 'Units and Types of Motion',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Evolution of transport',
      'Standard units of measurement (SI units)',
      'Types of motion: Rectilinear, Circular, Periodic'
    ],
    examples: ['1 metre = 100 cm', 'Motion of a swing (Periodic)'],
    misconceptions: ['Handspan is a standard unit of measurement'],
    practiceExercises: [
      PracticeExercise(
        question: 'The motion of a spinning top is an example of?',
        hint: 'It moves around an axis.',
        options: ['Rectilinear', 'Circular', 'Periodic', 'Random'],
        correctAnswer: 'Circular',
        explanation: 'An object moving in a circle or around an axis shows circular motion.'
      )
    ],
    flashcards: [
      Flashcard(front: '1 km', back: '1000 metres'),
      Flashcard(front: 'Rectilinear', back: 'Motion in a straight line')
    ],
    revisionNotes: 'Use standard units to avoid confusion in measurements.',
    commonMistakes: ['Measuring from the end of the ruler instead of 0 mark']
  ),

  's6_c8': const ConceptNode(
    id: 's6_c8',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Light, Shadows and Reflections',
    topic: 'Physics',
    subtopic: 'Optics Basics',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'How shadows are formed',
      'Difference between Image and Shadow',
      'Reflection from a mirror and Pinhole Camera'
    ],
    examples: ['Moon is a non-luminous object', 'Shadows are always black'],
    misconceptions: ['Shadows show the color of the object'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is required for a shadow to form?',
        hint: 'You need light and something that blocks it.',
        options: ['Light only', 'Screen only', 'Opaque object only', 'Light, Opaque object, and Screen'],
        correctAnswer: 'Light, Opaque object, and Screen',
        explanation: 'All three are necessary to see a shadow.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Luminous', back: 'Objects that emit their own light (e.g. Sun)'),
      Flashcard(front: 'Reflection', back: 'Bouncing back of light from a surface')
    ],
    revisionNotes: 'Light travels in a straight line.',
    commonMistakes: ['Thinking non-luminous objects cannot be seen']
  ),

  's6_c9': const ConceptNode(
    id: 's6_c9',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Electricity and Circuits',
    topic: 'Physics',
    subtopic: 'Circuits and Conductors',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand components of a simple circuit',
      'Identify Conductors and Insulators',
      'Function of a switch and an electric cell'
    ],
    examples: ['Copper is a conductor', 'Rubber is an insulator'],
    misconceptions: ['Electricity flows even if the circuit is open'],
    practiceExercises: [
      PracticeExercise(
        question: 'A device that breaks the circuit is called?',
        hint: 'You use it to turn lights on/off.',
        options: ['Battery', 'Switch', 'Bulb', 'Wire'],
        correctAnswer: 'Switch',
        explanation: 'A switch is a simple device that either breaks the circuit or completes it.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Filament', back: 'Tiny wire in a bulb that glows'),
      Flashcard(front: 'Terminals', back: 'Positive (+) and Negative (-) ends of a cell')
    ],
    revisionNotes: 'Electricity flows from positive to negative terminal.',
    commonMistakes: ['Touching electric wires with wet hands']
  ),

  's6_c10': const ConceptNode(
    id: 's6_c10',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Fun with Magnets',
    topic: 'Physics',
    subtopic: 'Magnetism',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Magnetic and non-magnetic materials',
      'Identify poles of a magnet',
      'Making your own magnet and magnetic compass'
    ],
    examples: ['Compass points North-South', 'Iron is magnetic'],
    misconceptions: ['Magnets can attract all metals (they don\'t attract Gold/Silver)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where is the attraction of a magnet strongest?',
        hint: 'At the ends.',
        options: ['Middle', 'North Pole only', 'Both Poles', 'Everywhere'],
        correctAnswer: 'Both Poles',
        explanation: 'Magnetic force is most concentrated at the North and South poles.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Repulsion', back: 'Similar poles push each other away'),
      Flashcard(front: 'Attraction', back: 'Opposite poles pull each other')
    ],
    revisionNotes: 'A freely suspended magnet always rests in N-S direction.',
    commonMistakes: ['Storing magnets incorrectly (leading to loss of magnetism)']
  ),

  's6_c11': const ConceptNode(
    id: 's6_c11',
    subject: 'Science',
    classLevel: 6,
    chapter: 'Air Around Us',
    topic: 'Chemistry',
    subtopic: 'Atmosphere and Gases',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Composition of Air (Nitrogen, Oxygen, etc.)',
      'Importance of the Atmosphere',
      'Availability of Oxygen to aquatic animals'
    ],
    examples: ['Windmill generating power', 'Breathing under water'],
    misconceptions: ['Air is empty space (it has mass and occupies space)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which gas is highest in percentage in our atmosphere?',
        hint: 'It is about 78%.',
        options: ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Argon'],
        correctAnswer: 'Nitrogen',
        explanation: 'Nitrogen makes up the majority of our air.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Atmosphere', back: 'Layer of air surrounding the earth'),
      Flashcard(front: 'Oxygen', back: 'Gas required for burning and breathing')
    ],
    revisionNotes: 'Air is essential for life on Earth. Plants and animals maintain balance of gases.',
    commonMistakes: ['Thinking air has only one gas']
  ),

  // ===========================================================================
  // CLASS 6 SOCIAL SCIENCE (Civics - Social and Political Life - I)
  // ===========================================================================

  'ss6_c1': const ConceptNode(
    id: 'ss6_c1',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Understanding Diversity',
    topic: 'Social Science',
    subtopic: 'Diversity in India',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the concept of diversity',
      'Learn about diversity in Ladakh and Kerala',
      'Unity in Diversity (Nehru\'s phrase)'
    ],
    examples: ['Different food, languages, religions', 'Story of Samir Ek and Samir Do'],
    misconceptions: ['Diversity means inequality (diversity is difference, inequality is unfairness)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who coined the phrase "Unity in Diversity"?',
        hint: 'He was India\'s first Prime Minister.',
        options: ['Gandhiji', 'Ambedkar', 'Jawaharlal Nehru', 'Sardar Patel'],
        correctAnswer: 'Jawaharlal Nehru',
        explanation: 'Nehru wrote about India\'s unity in his book "The Discovery of India".'
      )
    ],
    flashcards: [
      Flashcard(front: 'Ladakh Trade', back: 'Pashmina wool and Silk route connection'),
      Flashcard(front: 'Kerala Spices', back: 'Pepper, Cloves, Cardamoms')
    ],
    revisionNotes: 'India\'s diversity is its strength.',
    commonMistakes: ['Thinking diversity only means religion']
  ),

  'ss6_c2': const ConceptNode(
    id: 'ss6_c2',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Diversity and Discrimination',
    topic: 'Social Science',
    subtopic: 'Equality and Justice',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: ['e5_c16'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Difference between Prejudice and Stereotype',
      'Impact of discrimination on people\'s lives',
      'Constitutional fight for equality (Dr. Ambedkar)'
    ],
    examples: ['Stereotype: Boys don\'t cry', 'Prejudice: Negative opinions about rural people'],
    misconceptions: ['Stereotypes are always true'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is known as the Father of the Indian Constitution?',
        hint: 'He fought for Dalit rights.',
        options: ['Gandhiji', 'Dr. B.R. Ambedkar', 'Nehru', 'Radhakrishnan'],
        correctAnswer: 'Dr. B.R. Ambedkar',
        explanation: 'Ambedkar chaired the drafting committee and worked for equality.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Stereotype', back: 'Fixing people into one image based on group'),
      Flashcard(front: 'Discrimination', back: 'Acting on prejudices and treating people unfairly')
    ],
    revisionNotes: 'Equality is a value that we have to keep striving for.',
    commonMistakes: ['Confusing Prejudice with Discrimination']
  ),

  'ss6_c3': const ConceptNode(
    id: 'ss6_c3',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'What is Government?',
    topic: 'Political Science',
    subtopic: 'Governance and Democracy',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Functions of the government',
      'Levels of government: Local, State, National',
      'Types: Democracy and Monarchy'
    ],
    examples: ['Building roads', 'Printing currency', 'Elections'],
    misconceptions: ['Government is only the police (it includes all administrative bodies)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is a "Representative Democracy"?',
        hint: 'People choose their leaders.',
        options: ['King rules', 'People vote for representatives', 'Direct rule by people', 'Army rule'],
        correctAnswer: 'People vote for representatives',
        explanation: 'In most modern democracies, people don\'t rule directly but choose reps.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Suffrage', back: 'The right to vote in elections'),
      Flashcard(front: 'Monarchy', back: 'Rule by a King or Queen with final decision power')
    ],
    revisionNotes: 'Government makes laws and everyone living in the country has to follow them.',
    commonMistakes: ['Thinking state government handles national borders']
  ),

  'ss6_c4': const ConceptNode(
    id: 'ss6_c4',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Key Elements of a Democratic Government',
    topic: 'Political Science',
    subtopic: 'Participation and Conflict',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'People\'s participation in governance',
      'Resolving conflicts and promoting equality',
      'South Africa\'s struggle against Apartheid'
    ],
    examples: ['Rallies, protests, signature campaigns', 'Nelson Mandela'],
    misconceptions: ['Voting once is the only form of participation'],
    practiceExercises: [
      PracticeExercise(
        question: 'What was the policy of "Apartheid" in South Africa?',
        hint: 'Separation based on race.',
        options: ['Equality for all', 'Separation of races', 'Free education', 'Animal rights'],
        correctAnswer: 'Separation of races',
        explanation: 'Apartheid meant separation on the basis of race (Blacks, Whites, Indians, etc.).'
      )
    ],
    flashcards: [
      Flashcard(front: 'Conflict', back: 'When people of different groups don\'t agree'),
      Flashcard(front: 'ANC', back: 'African National Congress')
    ],
    revisionNotes: 'A democracy resolves conflicts through laws and discussions.',
    commonMistakes: ['Thinking all conflicts are bad for democracy']
  ),

  'ss6_c5': const ConceptNode(
    id: 'ss6_c5',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Panchayati Raj',
    topic: 'Local Governance',
    subtopic: 'Village Administration',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Functioning of Gram Sabha and Gram Panchayat',
      'Sources of funds for Panchayats',
      'Three levels of Panchayats (Gram, Block, Zila)'
    ],
    examples: ['Village water problems', 'BPL list approval'],
    misconceptions: ['Gram Sabha and Gram Panchayat are the same (Sabha is the assembly of all adults)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is the head of the Gram Panchayat?',
        hint: 'He is elected by members.',
        options: ['Collector', 'Sarpanch', 'Secretary', 'BDO'],
        correctAnswer: 'Sarpanch',
        explanation: 'The Panchayat members (Panches) elect a Sarpanch as the head.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Gram Sabha', back: 'Meeting of all adults who live in the area'),
      Flashcard(front: 'Zila Parishad', back: 'District level of the Panchayat system')
    ],
    revisionNotes: 'Panchayati Raj is the first tier of democratic government.',
    commonMistakes: ['Confusing the Secretary (govt appointed) with Sarpanch (elected)']
  ),

  'ss6_c6': const ConceptNode(
    id: 'ss6_c6',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Rural Administration',
    topic: 'Local Governance',
    subtopic: 'Police and Land Records',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Role of a Police Station (FIR)',
      'Maintenance of Land Records (Patwari)',
      'Hindu Succession Amendment Act 2005'
    ],
    examples: ['A dispute over a land boundary', 'Getting a copy of land map'],
    misconceptions: ['Only sons inherit father\'s property (laws have changed!)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the person in charge of a Police Station called?',
        hint: 'Abbreviation is S.H.O.',
        options: ['Patwari', 'Collector', 'Station House Officer', 'Jailor'],
        correctAnswer: 'Station House Officer',
        explanation: 'The SHO is the head of the local police station.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Patwari', back: 'Officer who measures land and keeps records'),
      Flashcard(front: 'Khasra', back: 'Register of land records kept by Patwari')
    ],
    revisionNotes: 'Patwari is also known as Lekhpal, Kanungo, or Village Officer in different states.',
    commonMistakes: ['Thinking the Collector does the day-to-day land measuring']
  ),

  'ss6_c7': const ConceptNode(
    id: 'ss6_c7',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Urban Administration',
    topic: 'Local Governance',
    subtopic: 'Municipal Corporations',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Role of Ward Councillors and Committees',
      'Functions of the Municipal Corporation/Council',
      'Waste management and cleanliness in cities'
    ],
    examples: ['Surat plague and cleanliness drive', 'Replaced street lights'],
    misconceptions: ['Ward Councillors are appointed by government (they are elected)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is the head of a Municipal Corporation?',
        hint: 'It starts with M.',
        options: ['Chairman', 'Mayor', 'Collector', 'Commissioner'],
        correctAnswer: 'Mayor',
        explanation: 'Large cities have a Mayor as the ceremonial head of the Corporation.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Municipal Commissioner', back: 'Officer who implements decisions (appointed)'),
      Flashcard(front: 'Ward', back: 'Division of a city for election purposes')
    ],
    revisionNotes: 'Property taxes provide money for city maintenance.',
    commonMistakes: ['Confusing Municipal Council (small towns) with Corporation (cities)']
  ),

  'ss6_c8': const ConceptNode(
    id: 'ss6_c8',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Rural Livelihoods',
    topic: 'Economics',
    subtopic: 'Farming and Labor',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['e5_c19'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Types of work in villages (Agricultural and Non-farming)',
      'Problems of small farmers and debt',
      'Life of landless laborers (Thulasi\'s story)'
    ],
    examples: ['Terrace farming in Nagaland', 'Fishing in coastal villages'],
    misconceptions: ['All villagers are farmers'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the main reason for farmer suicide in some regions?',
        hint: 'It involves borrowed money.',
        options: ['Bad weather', 'Debt/Loan burden', 'Lack of seeds', 'Laziness'],
        correctAnswer: 'Debt/Loan burden',
        explanation: 'Small farmers often take loans and if the crop fails, they fall into a debt trap.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Terrace Farming', back: 'Farming on carved steps on mountain slopes'),
      Flashcard(front: 'Paddy', back: 'Rice crop')
    ],
    revisionNotes: '40% of rural families in India are agricultural laborers.',
    commonMistakes: ['Thinking big farmers do all the manual work themselves']
  ),

  'ss6_c9': const ConceptNode(
    id: 'ss6_c9',
    subject: 'Civics',
    classLevel: 6,
    chapter: 'Urban Livelihoods',
    topic: 'Economics',
    subtopic: 'Service and Employment',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['e5_c22'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Self-employed workers on streets (vendors)',
      'Work in factories and casual labor',
      'Permanent vs Temporary jobs'
    ],
    examples: ['Call center workers', 'Rickshaw pullers', 'Marketing managers'],
    misconceptions: ['Street vendors don\'t contribute to economy'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which of these is a "Permanent Job"?',
        hint: 'It has benefits like PF and holidays.',
        options: ['Daily wage laborer', 'Street vendor', 'Bank employee', 'Casual painter'],
        correctAnswer: 'Bank employee',
        explanation: 'Permanent jobs provide job security and benefits like health insurance.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Call Center', back: 'Centralized office that handles high volume of calls'),
      Flashcard(front: 'Labour Chowk', back: 'Place where daily wage workers wait for work')
    ],
    revisionNotes: 'Cities provide many opportunities but also many challenges for workers.',
    commonMistakes: ['Thinking all office jobs are permanent']
  ),

  // ===========================================================================
  // CLASS 6 ENGLISH (Honeysuckle)
  // ===========================================================================

  'en6_c1': const ConceptNode(
    id: 'en6_c1',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 1: Who Did Patrick’s Homework? / A House, A Home',
    topic: 'Literature',
    subtopic: 'Values and Self-reliance',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn the value of hard work and self-help',
      'Understand the difference between a house (structure) and a home (family)',
      'Vocabulary: Britches, Elf, Glitch'
    ],
    examples: ['Patrick being lazy', 'The little elf "helping" him', 'Family love in a home'],
    misconceptions: ['The elf did all the work (Patrick actually did it while helping the elf)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What did Patrick think his cat was playing with?',
        hint: 'It was a tiny person.',
        options: ['A ball', 'A little doll', 'A mouse', 'A piece of cloth'],
        correctAnswer: 'A little doll',
        explanation: 'Patrick thought it was a doll, but it was actually a man of the tiniest size (an elf).'
      )
    ],
    flashcards: [
      Flashcard(front: 'Ignoramus', back: 'An ignorant person who lacks education'),
      Flashcard(front: 'A Home is made of?', back: 'Unselfish acts, brothers, sisters, fathers, mothers')
    ],
    revisionNotes: 'Self-help is the best help. Patrick changed his attitude towards work.',
    commonMistakes: ['Confusing "house" and "home" definitions']
  ),

  'en6_c2': const ConceptNode(
    id: 'en6_c2',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 2: How the Dog Found Himself a New Master! / The Kite',
    topic: 'Literature',
    subtopic: 'Discovery and Nature',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Narrative of animal domestication (folklore)',
      'Appreciate the movement and beauty of a kite',
      'Vocabulary: Kinsman, Snort, Panic'
    ],
    examples: ['Dog following Wolf, Bear, Lion', 'Dog finally choosing Man', 'A new kite snapping on a string'],
    misconceptions: ['Dogs were always pets (they were once wild)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why did the dog finally choose Man as his master?',
        hint: 'The Lion was afraid of Man.',
        options: ['Man is kind', 'Man is the strongest', 'Man has food', 'Man is fast'],
        correctAnswer: 'Man is the strongest',
        explanation: 'The dog wanted a master who was the strongest on earth, and he saw even the Lion feared Man.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Kinsman', back: 'A relative'),
      Flashcard(front: 'Raggeder', back: 'More torn or worn out (like a stuck kite)')
    ],
    revisionNotes: 'The dog found man to be the most powerful master. A kite looks bright when new.',
    commonMistakes: ['Confusing the order of masters the dog tried']
  ),

  'en6_c3': const ConceptNode(
    id: 'en6_c3',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 3: Taro’s Reward / The Quarrel',
    topic: 'Value Education',
    subtopic: 'Filial Piety and Conflict',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Japanese folklore and rewards for virtue',
      'Understand the nature of sibling quarrels',
      'Vocabulary: Sake, Chopped, Mutters'
    ],
    examples: ['Magic waterfall giving Sake to Taro', 'Waterfall giving plain water to greedy neighbors'],
    misconceptions: ['Quarrels always have a clear reason (sometimes we don\'t even know why they start!)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What did the waterfall give to Taro?',
        hint: 'A delicious Japanese drink.',
        options: ['Cold water', 'Hot tea', 'Delicious Sake', 'Milk'],
        correctAnswer: 'Delicious Sake',
        explanation: 'Because Taro was a thoughtful son, the magic waterfall gave him Sake.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Sake', back: 'A popular Japanese drink'),
      Flashcard(front: 'Quarrel outcome', back: 'The afternoon turned black, but they made up by night')
    ],
    revisionNotes: 'Kindness and devotion to parents are always rewarded.',
    commonMistakes: ['Thinking Taro was greedy']
  ),

  'en6_c4': const ConceptNode(
    id: 'en6_c4',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 4: Kalpana Chawla / Beauty',
    topic: 'Biography',
    subtopic: 'Inspiration and Aesthetics',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['e5_c11'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Life and achievements of Kalpana Chawla',
      'Understand that beauty is internal and in deeds',
      'Vocabulary: Astronaut, Space shuttle, Disaster'
    ],
    examples: ['Columbia space shuttle', 'Beauty in the corn growing and people working'],
    misconceptions: ['Kalpana was born in the USA (she was born in Karnal, India)'],
    practiceExercises: [
      PracticeExercise(
        question: 'In which year did the Columbia disaster happen?',
        hint: 'It was early 2000s.',
        options: ['1997', '2003', '2005', '2001'],
        correctAnswer: '2003',
        explanation: 'Space Shuttle Columbia broke apart on 1st Feb 2003.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Space Shuttle', back: 'Spacecraft used for repeated journeys between Earth and station'),
      Flashcard(front: 'Beauty is heard in?', back: 'Wind sighing, rain falling, or a singer chanting')
    ],
    revisionNotes: 'Nothing is impossible if you have a dream and the courage to follow it.',
    commonMistakes: ['Spelling of "Columbia"']
  ),

  'en6_c5': const ConceptNode(
    id: 'en6_c5',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 5: A Different Kind of School / Where Do All the Teachers Go?',
    topic: 'Literature',
    subtopic: 'Empathy and Curiosity',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['h5_c9'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn the value of "blind day" and "dumb day" to feel empathy',
      'Understand a child\'s curiosity about teachers\' personal lives',
      'Vocabulary: Ghastly, Misfortune, Crutch'
    ],
    examples: ['Miss Beam\'s school', 'Children with bandaged eyes'],
    misconceptions: ['The children were actually disabled (they were practicing being disabled for a day)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What was the main aim of Miss Beam\'s school?',
        hint: 'It wasn\'t just about math or science.',
        options: ['To make athletes', 'To teach thoughtfullness and kindness', 'To win awards', 'To be strict'],
        correctAnswer: 'To teach thoughtfullness and kindness',
        explanation: 'She wanted children to be "responsible citizens" who understand others\' pain.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Empathy', back: 'Understanding and sharing the feelings of another'),
      Flashcard(front: 'The poem\'s theme', back: 'Child\'s wonder if teachers are ordinary people too')
    ],
    revisionNotes: 'Experiencing a problem helps us respect those who live with it every day.',
    commonMistakes: ['Thinking the school was cruel']
  ),

  'en6_c6': const ConceptNode(
    id: 'en6_c6',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 6: Who I Am / The Wonderful Words',
    topic: 'Self and Language',
    subtopic: 'Identity and Expression',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Appreciate diversity in human interests and dreams',
      'Understand the power of words and language',
      'Vocabulary: Rafting, Preserved, Marvel'
    ],
    examples: ['Radha (climbing trees)', 'Peter (movies)', 'Language as the "dress of thought"'],
    misconceptions: ['Words are just sounds (they are the only way to release thoughts)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who wants to be a "seed collector"?',
        hint: 'A boy in the chapter.',
        options: ['Nasir', 'Rohit', 'Peter', 'Dolma'],
        correctAnswer: 'Nasir',
        explanation: 'Nasir wants to learn how to preserve seeds to help his grandfather.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Language', back: 'The dress of thought'),
      Flashcard(front: 'Dolma\'s dream', back: 'To be the Prime Minister of India')
    ],
    revisionNotes: 'Everyone is unique with different strengths and goals.',
    commonMistakes: ['Mixing up the children\'s names and their dreams']
  ),

  'en6_c7': const ConceptNode(
    id: 'en6_c7',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 7: Fair Play',
    topic: 'Social Science and Drama',
    subtopic: 'Justice and Friendship',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 60),
    prerequisites: ['ss6_c5'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the role of the Panchayat in villages',
      'The principle that "The Voice of the Panch is the Voice of God"',
      'Vocabulary: Property, Culprit, Reluctant'
    ],
    examples: ['Jumman Sheikh and Algu Chowdhury', 'The aunt\'s case'],
    misconceptions: ['Friends should support each other even in wrong acts'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who was appointed as the Head Panch by the aunt?',
        hint: 'Jumman\'s best friend.',
        options: ['Jumman', 'Algu Chowdhury', 'Samjhu Sahu', 'The Village Head'],
        correctAnswer: 'Algu Chowdhury',
        explanation: 'The aunt chose Algu, trusting his honesty despite his friendship with Jumman.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Panchayat', back: 'A village council that settles disputes'),
      Flashcard(front: 'Moral of Fair Play', back: 'Justice should come before friendship')
    ],
    revisionNotes: 'A person on the seat of a judge has no friend or enemy, only the truth.',
    commonMistakes: ['Thinking Algu was mean to Jumman']
  ),

  'en6_c8': const ConceptNode(
    id: 'en6_c8',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 8: A Game of Chance / Vocation',
    topic: 'Literature',
    subtopic: 'Fairness and Desires',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about fair ground tricks and luck',
      'Appreciate different vocations (Hawker, Gardener, Watchman)',
      'Vocabulary: Disappointed, Trifle, Chasing'
    ],
    examples: ['Lucky Shop at the Eid fair', 'Rashid losing money', 'Child wishing to be a watchman'],
    misconceptions: ['"Game of Chance" shops are honest (they are often fixed to trick people)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why was Rashid upset after the fair?',
        hint: 'He played the Lucky Shop.',
        options: ['He lost his way', 'He lost all his money', 'He didn\'t get a toy', 'His uncle scolded him'],
        correctAnswer: 'He lost all his money',
        explanation: 'He was tricked into thinking he was unlucky, while the shopkeeper was cheating.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Vocation', back: 'A person\'s trade or profession'),
      Flashcard(front: 'Gong', back: 'A metal disk that makes a sound when struck')
    ],
    revisionNotes: 'Don\'t be fooled by the lure of easy money. Every job has its own life.',
    commonMistakes: ['Confusing the vocations in the poem']
  ),

  'en6_c9': const ConceptNode(
    id: 'en6_c9',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 9: Desert Animals / Whatif',
    topic: 'Science and Emotions',
    subtopic: 'Adaptation and Anxiety',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: ['s6_c6'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn how animals survive in deserts (Camels, Snakes, Gerbils)',
      'Handle "What if" anxious thoughts',
      'Vocabulary: Dunes, Scorching, Slither'
    ],
    examples: ['Rattlesnake warning', 'Camel\'s humps (storing fat, not water)'],
    misconceptions: ['Camels store water in their humps (it is fat!)'],
    practiceExercises: [
      PracticeExercise(
        question: 'How many litres of water can a thirsty camel drink in ten minutes?',
        hint: 'It is a huge amount.',
        options: ['10 litres', '30 litres', '100 litres', '50 litres'],
        correctAnswer: '100 litres',
        explanation: 'A camel can drink about 30 gallons (100 litres) in just 10 mins.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Gila Monster', back: 'A poisonous lizard found in American deserts'),
      Flashcard(front: 'Whatif thoughts', back: 'Anxious worries that come at night')
    ],
    revisionNotes: 'Deserts are not just sand; they have a rich variety of life. Everyone has worries.',
    commonMistakes: ['Thinking snakes can hear (they feel vibrations)']
  ),

  'en6_c10': const ConceptNode(
    id: 'en6_c10',
    subject: 'English',
    classLevel: 6,
    chapter: 'Unit 10: The Banyan Tree',
    topic: 'Nature',
    subtopic: 'Observation and Wildlife',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about the ecosystem of a banyan tree',
      'Classic battle between Cobra and Mongoose',
      'Vocabulary: Prop, Magnificence, Aggressive'
    ],
    examples: ['Squirrels and birds in the tree', 'The grey mongoose vs black cobra'],
    misconceptions: ['The mongoose is immune to snake venom (it is just very fast)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who were the two "uninvited" spectators of the fight?',
        hint: 'A bird and an animal.',
        options: ['Myna and Crow', 'Cat and Dog', 'Parrot and Eagle', 'Owl and Rat'],
        correctAnswer: 'Myna and Crow',
        explanation: 'A myna and a jungle crow sat on a cactus to watch the battle.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Banyan tree age', back: 'Older than the house, as old as the town'),
      Flashcard(front: 'Mongoose weapon', back: 'Speed and agility')
    ],
    revisionNotes: 'Nature has its own laws of survival. The banyan tree is a world in itself.',
    commonMistakes: ['Thinking the crow survived the fight (it was bitten by the cobra)']
  ),

  // ===========================================================================
  // CLASS 6 HINDI (Vasant)
  // ===========================================================================

  'h6_c1': const ConceptNode(
    id: 'h6_c1',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Vah Chidiya Jo',
    topic: 'Poetry',
    subtopic: 'Nature and Freedom',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the desire for freedom through a bird',
      'Appreciate the beauty of nature and rivers',
      'Vocabulary: Santoshi, Garvili, Jundi'
    ],
    examples: ['Bird eating Jundi grains', 'Bird drinking from the overflowing river'],
    misconceptions: ['The bird is real (it is a symbol of human qualities like self-respect)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which river is mentioned in the poem?',
        hint: 'The bird drinks water from it.',
        options: ['Ganga', 'Yamuna', 'Chadhi Nadi', 'Narmada'],
        correctAnswer: 'Chadhi Nadi',
        explanation: 'The poet uses "Chadhi Nadi" to describe an overflowing, powerful river.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Santoshi', back: 'Contented / Satisfied'),
      Flashcard(front: 'Garvili', back: 'Proud (in a positive way)')
    ],
    revisionNotes: 'The poem emphasizes contentment and love for freedom.',
    commonMistakes: ['Thinking the bird is a specific species']
  ),

  'h6_c2': const ConceptNode(
    id: 'h6_c2',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Bachpan',
    topic: 'Literature',
    subtopic: 'Memories and Change',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Recall childhood memories (Krishna Sobti)',
      'Compare old times with modern times',
      'Vocabulary: Siyahi, Shani-Ravivar, Gramophone'
    ],
    examples: ['Drinking castor oil on Sundays', 'First time wearing spectacles'],
    misconceptions: ['Old times were boring without mobile phones'],
    practiceExercises: [
      PracticeExercise(
        question: 'What did the author have to drink every Sunday morning?',
        hint: 'It was for health.',
        options: ['Milk', 'Castor Oil', 'Juice', 'Tea'],
        correctAnswer: 'Castor Oil',
        explanation: 'The author mentions taking olive oil or castor oil for health on Sundays.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Gramophone', back: 'An old device used for playing music'),
      Flashcard(front: 'Convent School', back: 'Type of school mentioned in memories')
    ],
    revisionNotes: 'Lifestyles change with time, but childhood joys remain universal.',
    commonMistakes: ['Thinking the author is a man']
  ),

  'h6_c3': const ConceptNode(
    id: 'h6_c3',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Nadan Dost',
    topic: 'Literature',
    subtopic: 'Children and Animals',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the curiosity of children towards nature',
      'Learn about animal behavior (birds and eggs)',
      'Moral lesson on unintended harm'
    ],
    examples: ['Keshav and Shyama', 'Cornice of the house'],
    misconceptions: ['Birds will be happy if we provide them a bed/cushion (they might desert the eggs if humans touch them)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Why did the bird break her own eggs?',
        hint: 'Humans touched them.',
        options: ['They were bad', 'Because they became dirty (human touch)', 'By mistake', 'To eat them'],
        correctAnswer: 'Because they became dirty (human touch)',
        explanation: 'Once humans touch bird eggs, the mother often leaves or breaks them.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Nadan', back: 'Innocent / Foolish'),
      Flashcard(front: 'Cornice', back: 'A horizontal decorative molding')
    ],
    revisionNotes: 'Love for animals should be combined with knowledge of their nature.',
    commonMistakes: ['Thinking Keshav was mean to the birds']
  ),

  'h6_c4': const ConceptNode(
    id: 'h6_c4',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Chand se Thodi si Gappe',
    topic: 'Poetry',
    subtopic: 'Imagination',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.create,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Enjoy the whimsical imagination of a child',
      'Learn about the phases of the moon in poetic language',
      'Vocabulary: Akas, Kul, Tirchi'
    ],
    examples: ['Stars as a dress for the moon', 'Moon growing and shrinking as a disease'],
    misconceptions: ['The moon is actually sick (it is just a child\'s perspective)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What does the child think the moon\'s "dress" is made of?',
        hint: 'Look at the night sky.',
        options: ['Cloud', 'Stars', 'Silk', 'Silver'],
        correctAnswer: 'Stars',
        explanation: 'The child imagines the moon wearing the entire sky studded with stars.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Akas', back: 'Sky'),
      Flashcard(front: 'Kul', back: 'Total / Entire')
    ],
    revisionNotes: 'Poetry allows us to see common things in extraordinary ways.',
    commonMistakes: ['Mixing up the waxing and waning phases']
  ),

  'h6_c5': const ConceptNode(
    id: 'h6_c5',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Aksharon ka Mahatva',
    topic: 'History',
    subtopic: 'Evolution of Script',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['ss6_h1'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the importance of letters and script',
      'History of human communication',
      'Difference between Prehistory and History'
    ],
    examples: ['Ideograms (picture signs)', 'Discovery of writing 6000 years ago'],
    misconceptions: ['Letters were created by God (they were invented by humans)'],
    practiceExercises: [
      PracticeExercise(
        question: 'When did the history of mankind begin?',
        hint: 'When we started writing.',
        options: ['1 million years ago', 'When letters were invented', 'When fire was discovered', 'With the wheel'],
        correctAnswer: 'When letters were invented',
        explanation: 'History begins when we can read what people wrote in the past.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Pragaitihasik', back: 'Prehistoric (before written records)'),
      Flashcard(front: 'Lipya', back: 'Scripts')
    ],
    revisionNotes: 'Writing allowed humans to store knowledge and pass it to generations.',
    commonMistakes: ['Thinking alphabets were always there']
  ),

  'h6_c6': const ConceptNode(
    id: 'h6_c6',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Par Nazar ke',
    topic: 'Science Fiction',
    subtopic: 'Life on Mars',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Explore the genre of science fiction',
      'Imagining underground life on Mars',
      'Handling curiosity and rules'
    ],
    examples: ['Chhotu using father\'s security card', 'Viking mission to Mars'],
    misconceptions: ['Mars is currently inhabited by underground people'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where did Chhotu\'s family live?',
        hint: 'It was for protection from the surface.',
        options: ['In a forest', 'Under the surface of Mars', 'On the Moon', 'In a city like Delhi'],
        correctAnswer: 'Under the surface of Mars',
        explanation: 'In the story, life on the surface became impossible, so they moved underground.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Yantra', back: 'Machine / Instrument'),
      Flashcard(front: 'Viking', back: 'Real-life NASA mission to Mars mentioned in the chapter')
    ],
    revisionNotes: 'Science fiction combines scientific facts with imaginative storytelling.',
    commonMistakes: ['Confusing the fictional story with scientific reality']
  ),

  'h6_c7': const ConceptNode(
    id: 'h6_c7',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Sathi Hath Badhana',
    topic: 'Poetry',
    subtopic: 'Unity and Labor',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: ['en5_c2'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Value of collective effort',
      'Inspiration for hard-working people',
      'Hindi vocabulary related to strength'
    ],
    examples: ['Building a road together', 'Turning mountains into paths'],
    misconceptions: ['One hero does everything alone'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is the poet of "Sathi Hath Badhana"?',
        hint: 'A famous lyricist.',
        options: ['Sahir Ludhianvi', 'Gulzar', 'Javed Akhtar', 'Bachchan'],
        correctAnswer: 'Sahir Ludhianvi',
        explanation: 'This inspiring song/poem was written by Sahir Ludhianvi.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Fauladi', back: 'Made of steel / Very strong'),
      Flashcard(front: 'Naseeb', back: 'Fate / Destiny')
    ],
    revisionNotes: 'Work becomes light and successful when everyone helps.',
    commonMistakes: ['Thinking the poem is only for laborers']
  ),

  'h6_c8': const ConceptNode(
    id: 'h6_c8',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Aise-Aise',
    topic: 'Drama',
    subtopic: 'Humour and Excuses',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 3,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Humorous take on children\'s fear of homework',
      'Structure of a one-act play (Ekanki)',
      'Understanding character roles'
    ],
    examples: ['Mohan pretending to have a stomach ache', 'The Doctor and Vaidya visiting'],
    misconceptions: ['Mohan had a real illness'],
    practiceExercises: [
      PracticeExercise(
        question: 'What was the "Aise-Aise" disease?',
        hint: 'It wasn\'t real.',
        options: ['Stomach flu', 'Fear of homework', 'Headache', 'Fever'],
        correctAnswer: 'Fear of homework',
        explanation: 'Mohan didn\'t finish his school work, so he made an excuse using "Aise-Aise".'
      )
    ],
    flashcards: [
      Flashcard(front: 'Ekanki', back: 'A one-act play'),
      Flashcard(front: 'Vaidya Ji', back: 'Traditional Indian doctor')
    ],
    revisionNotes: 'Honesty with teachers and parents avoids unnecessary drama.',
    commonMistakes: ['Missing the comic timing of the play']
  ),

  'h6_c9': const ConceptNode(
    id: 'h6_c9',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Ticket Album',
    topic: 'Story',
    subtopic: 'Envy and Friendship',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the feeling of jealousy and regret',
      'Learn about the hobby of philately (stamp collecting)',
      'Moral value of confession and honesty'
    ],
    examples: ['Rajappa burning Nagarajan\'s album', 'Rajappa giving his own album in the end'],
    misconceptions: ['Rajappa was a "bad" person (he was just overwhelmed by envy)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who got a ticket album from Singapore?',
        hint: 'The popular boy.',
        options: ['Rajappa', 'Nagarajan', 'Krishna', 'Appu'],
        correctAnswer: 'Nagarajan',
        explanation: 'Nagarajan\'s uncle sent him a beautiful album from Singapore.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Irshya', back: 'Jealousy / Envy'),
      Flashcard(front: 'Pashchatap', back: 'Regret / Remorse')
    ],
    revisionNotes: 'Envy can make a person do wrong things, but true courage lies in accepting mistakes.',
    commonMistakes: ['Thinking Rajappa stole the album to sell it']
  ),

  'h6_c10': const ConceptNode(
    id: 'h6_c10',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Jhansi ki Rani',
    topic: 'Poetry',
    subtopic: 'Bravery and Freedom',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.understand,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Biography of Laxmi Bai in verse',
      'Understand the 1857 revolt against British',
      'Vocabulary: Veer-gatha, Dalhousie, Inquilab'
    ],
    examples: ['Laxmi Bai playing with dolls vs swords', 'Fighting like a man (Khoob ladi mardani)'],
    misconceptions: ['Jhansi was the only state that fought (many fought, but Jhansi was legendary)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is the author of this poem?',
        hint: 'Same as "Khilaunewala".',
        options: ['Mahadevi Verma', 'Subhadra Kumari Chauhan', 'Sarojini Naidu', 'Prasad'],
        correctAnswer: 'Subhadra Kumari Chauhan',
        explanation: 'Subhadra Kumari Chauhan wrote this famous patriotic poem.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Chhabili', back: 'Laxmi Bai\'s childhood name'),
      Flashcard(front: 'Birsingha', back: 'Bundelkhandi bard mentioned in poem')
    ],
    revisionNotes: 'The Queen of Jhansi was one of the greatest heroes of India\'s first war of independence.',
    commonMistakes: ['Spelling of "Subhadra Kumari Chauhan"']
  ),

  'h6_c11': const ConceptNode(
    id: 'h6_c11',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Jo Dekhkar bhi nahi Dekhte',
    topic: 'Literature',
    subtopic: 'Perception and Gratitude',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Understand the perspective of a visually impaired person (Helen Keller)',
      'Learn to appreciate nature using other senses',
      'Value of being grateful for our abilities'
    ],
    examples: ['Feeling the texture of birch tree bark', 'Listening to bird songs'],
    misconceptions: ['Blind people cannot enjoy the beauty of nature'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is the author of this essay?',
        hint: 'A world-famous deaf-blind author.',
        options: ['Krishna Sobti', 'Helen Keller', 'Premchand', 'Tagore'],
        correctAnswer: 'Helen Keller',
        explanation: 'Helen Keller shares how she "sees" nature through touch and smell.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Anubhuti', back: 'Feeling / Experience'),
      Flashcard(front: 'Samvedna', back: 'Sensitivity / Empathy')
    ],
    revisionNotes: 'We often take our senses for granted, while those who lack them value them more.',
    commonMistakes: ['Thinking Helen Keller was born deaf-blind (she became so after illness)']
  ),

  'h6_c12': const ConceptNode(
    id: 'h6_c12',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Sansar Pustak Hai',
    topic: 'Literature',
    subtopic: 'Nature and Science',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about Nehru\'s letters to his daughter Indira',
      'Nature as a giant book we should learn to read',
      'Formation of stones, pebbles, and sand'
    ],
    examples: ['A small pebble tells a story of its long journey', 'Pebble becoming sand over time'],
    misconceptions: ['Stones are just dead objects with no story'],
    practiceExercises: [
      PracticeExercise(
        question: 'To whom did Jawaharlal Nehru write these letters?',
        hint: 'His daughter.',
        options: ['Sonia', 'Indira Gandhi', 'Vijaya Lakshmi', 'Priyanka'],
        correctAnswer: 'Indira Gandhi',
        explanation: 'Nehru wrote these letters when Indira was 10 years old and in Mussoorie.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Ghor', back: 'Deep / Intense'),
      Flashcard(front: 'Kankad', back: 'Pebble')
    ],
    revisionNotes: 'The Earth is very old, and to understand its history, we must read the signs in nature.',
    commonMistakes: ['Thinking these were formal academic articles']
  ),

  'h6_c13': const ConceptNode(
    id: 'h6_c13',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Main Sabse Chhoti Hun',
    topic: 'Poetry',
    subtopic: 'Mother and Childhood',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 4,
    estStudyTime: const Duration(minutes: 30),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Enjoy the sweet bond between mother and child',
      'Desire to remain small to never lose mother\'s proximity',
      'Vocabulary: Aanchal, Chhalna, Sneh'
    ],
    examples: ['Holding mother\'s hand always', 'Listening to stories in mother\'s lap'],
    misconceptions: ['The child hates growing up (it\'s just a metaphor for love)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who is the poet of "Main Sabse Chhoti Hun"?',
        hint: 'He is a famous Chhayavadi poet.',
        options: ['Sumitranandan Pant', 'Nirala', 'Prasad', 'Verma'],
        correctAnswer: 'Sumitranandan Pant',
        explanation: 'Sumitranandan Pant wrote this beautiful poem about a child\'s love.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Aanchal', back: 'Corner of a sari / Mother\'s protection'),
      Flashcard(front: 'Nishhal', back: 'Pure / Innocent')
    ],
    revisionNotes: 'The poet expresses the purest form of love and dependence on a mother.',
    commonMistakes: ['Misidentifying the poet']
  ),

  'h6_c14': const ConceptNode(
    id: 'h6_c14',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Lokgeet',
    topic: 'Culture',
    subtopic: 'Folk Music of India',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['h5_c2'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about the diversity of Indian folk songs',
      'Instruments used in folk music (Dholak, Kartal)',
      'Social importance of community singing'
    ],
    examples: ['Bidesiya (Bihar)', 'Baul (Bengal)', 'Garba (Gujarat)'],
    misconceptions: ['Folk songs are only for villages (they are the soul of our culture)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which of these is a famous folk song of Bihar?',
        hint: 'It starts with B.',
        options: ['Kajri', 'Bidesiya', 'Lavani', 'Bhangra'],
        correctAnswer: 'Bidesiya',
        explanation: 'Bidesiya is a very popular folk song in Bhojpuri speaking regions.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Shastriya Sangeet', back: 'Classical Music'),
      Flashcard(front: 'Heer-Ranjha', back: 'Folk songs of Punjab')
    ],
    revisionNotes: 'Folk songs are flexible and change with the people who sing them.',
    commonMistakes: ['Thinking folk music needs expensive electronic instruments']
  ),

  'h6_c15': const ConceptNode(
    id: 'h6_c15',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Naukar',
    topic: 'Biography',
    subtopic: 'Service and Simplicity',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['e5_c16'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about Gandhiji\'s self-reliance',
      'Value of doing one\'s own work',
      'Respect for physical labor'
    ],
    examples: ['Gandhiji grinding flour', 'Gandhiji cleaning toilets', 'Caring for guests'],
    misconceptions: ['Leaders don\'t need to do manual work'],
    practiceExercises: [
      PracticeExercise(
        question: 'In which ashram did Gandhiji set examples of self-work?',
        hint: 'Near Ahmedabad.',
        options: ['Sabarmati Ashram', 'Sevagram', 'Both', 'None'],
        correctAnswer: 'Both',
        explanation: 'Gandhiji lived a simple life of labor in all his ashrams.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Svavalamban', back: 'Self-reliance'),
      Flashcard(front: 'Kasturba', back: 'Gandhiji\'s wife who supported him in simple life')
    ],
    revisionNotes: 'No work is low if done with devotion and honesty.',
    commonMistakes: ['Thinking Gandhiji was forced to do this work']
  ),

  'h6_c16': const ConceptNode(
    id: 'h6_c16',
    subject: 'Hindi',
    classLevel: 6,
    chapter: 'Van ke Marg Mein',
    topic: 'Poetry',
    subtopic: 'Ramayana and Devotion',
    difficulty: Difficulty.advanced,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Appreciate Tulsidas\'s Brajbhasha/Awadhi poetry',
      'Story of Ram, Sita, and Laxman going to exile',
      'Expressions of exhaustion and love'
    ],
    examples: ['Sita getting tired after a few steps', 'Ram shedding tears seeing her state'],
    misconceptions: ['Sita was weak (she was a princess who chose a difficult path for love)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who wrote the verses in "Van ke Marg Mein"?',
        hint: 'The author of Ramcharitmanas.',
        options: ['Kabir', 'Surdas', 'Tulsidas', 'Raskhan'],
        correctAnswer: 'Tulsidas',
        explanation: 'Goswami Tulsidas composed these beautiful verses.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Savaiya', back: 'The poetic meter used in this chapter'),
      Flashcard(front: 'Kanya', back: 'Princess (Sita)')
    ],
    revisionNotes: 'The poem beautifully captures the initial hardships of the forest journey.',
    commonMistakes: ['Thinking this is modern Hindi (it is older dialect)']
  ),

  'ss6_h1': const ConceptNode(
    id: 'ss6_h1',
    subject: 'History',
    classLevel: 6,
    chapter: 'What, Where, How and When?',
    topic: 'Historical Methodology',
    subtopic: 'Archaeology and Sources',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about river valley civilizations (Narmada, Indus, Ganga)',
      'Difference between Manuscripts and Inscriptions',
      'Understand dates (BC/AD or BCE/CE)'
    ],
    examples: ['Manuscripts on palm leaves', 'Inscriptions on stone/metal'],
    misconceptions: ['History is only about Kings (it is about common people too)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where did people first start living near rivers in India?',
        hint: 'Narmada is one of them.',
        options: ['Narmada valley', 'Thar desert', 'Himalayas', 'Deccan plateau'],
        correctAnswer: 'Narmada valley',
        explanation: 'People lived along the banks of Narmada for several hundred thousand years.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Manuscript', back: 'Books written by hand (Latin "Manu" means hand)'),
      Flashcard(front: 'Archaeologist', back: 'One who studies objects from the past')
    ],
    revisionNotes: 'History helps us understand how our ancestors lived.',
    commonMistakes: ['Confusing AD with "After Death" (it is Anno Domini)']
  ),

  'ss6_h2': const ConceptNode(
    id: 'ss6_h2',
    subject: 'History',
    classLevel: 6,
    chapter: 'From Hunting-Gathering to Growing Food',
    topic: 'Prehistory',
    subtopic: 'Neolithic Revolution',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Lifestyle of hunter-gatherers',
      'Discovery of fire and its uses',
      'The transition to farming and herding'
    ],
    examples: ['Bhimbetka caves (MP)', 'Mehrgarh (Pakistan)'],
    misconceptions: ['Farming happened overnight (it was a gradual process over thousands of years)'],
    practiceExercises: [
      PracticeExercise(
        question: 'In which site was fire first evidence found?',
        hint: 'It is a cave site.',
        options: ['Bhimbetka', 'Kurnool caves', 'Mehrgarh', 'Burzahom'],
        correctAnswer: 'Kurnool caves',
        explanation: 'Traces of ash have been found here, suggesting use of fire.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Domestication', back: 'Process of tending plants and animals for human use'),
      Flashcard(front: 'Burzahom', back: 'Site in Kashmir known for pit-houses')
    ],
    revisionNotes: 'Stone ages: Palaeolithic, Mesolithic, Neolithic.',
    commonMistakes: ['Thinking hunter-gatherers lived in one place']
  ),

  'ss6_h3': const ConceptNode(
    id: 'ss6_h3',
    subject: 'History',
    classLevel: 6,
    chapter: 'In the Earliest Cities',
    topic: 'Ancient Civilizations',
    subtopic: 'Harappan Civilization',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.analyze,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: ['e5_c10'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Unique features of Harappan cities (Citadel, Lower Town)',
      'Drainage system and urban planning',
      'Harappan crafts, trade, and mystery of decline'
    ],
    examples: ['Great Bath in Mohenjodaro', 'Terracotta toys', 'Seals'],
    misconceptions: ['Harappans had no writing system (they had a script, but it\'s undeciphered)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where was the "Great Bath" found?',
        hint: 'A major Harappan city.',
        options: ['Harappa', 'Mohenjodaro', 'Lothal', 'Dholavira'],
        correctAnswer: 'Mohenjodaro',
        explanation: 'The Great Bath was a special tank lined with bricks and plaster.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Citadel', back: 'The higher, smaller western part of a Harappan city'),
      Flashcard(front: 'Lothal', back: 'Harappan city in Gujarat with a dockyard')
    ],
    revisionNotes: 'Harappan cities were famous for baked bricks and planned streets.',
    commonMistakes: ['Confusing the Citadel with the Lower Town']
  ),

  'ss6_h4': const ConceptNode(
    id: 'ss6_h4',
    subject: 'History',
    classLevel: 6,
    chapter: 'What Books and Burials Tell Us',
    topic: 'Ancient India',
    subtopic: 'Vedas and Megaliths',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'About the four Vedas (Rigveda, Samaveda, Yajurveda, Atharvaveda)',
      'Social differences observed in burials',
      'Importance of Horses and Chariots in Vedic times'
    ],
    examples: ['Megaliths at Inamgaon', 'Suktas (hymns)'],
    misconceptions: ['Vedas were written down immediately (they were oral for centuries)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which is the oldest Veda?',
        hint: 'It has more than 1000 hymns.',
        options: ['Rigveda', 'Samaveda', 'Yajurveda', 'Atharvaveda'],
        correctAnswer: 'Rigveda',
        explanation: 'The Rigveda was composed about 3500 years ago.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Megalith', back: 'Big stones used to mark burial sites'),
      Flashcard(front: 'Sanskrit', back: 'Part of the Indo-European language family')
    ],
    revisionNotes: 'Burials often contain objects that suggest the person\'s status.',
    commonMistakes: ['Confusing Vedic culture with Harappan culture']
  ),

  'ss6_h5': const ConceptNode(
    id: 'ss6_h5',
    subject: 'History',
    classLevel: 6,
    chapter: 'Kingdoms, Kings and an Early Republic',
    topic: 'Political History',
    subtopic: 'Janapadas and Mahajanapadas',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Process of becoming a Raja (Ashvamedha sacrifice)',
      'Life in Mahajanapadas (Magadha, Vajji)',
      'Taxation and changes in agriculture'
    ],
    examples: ['Vajji Gana-sangha', 'The fortress of Magadha'],
    misconceptions: ['All ancient kingdoms were monarchies (some were Ganas/Republics)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What was the capital of the Vajji gana?',
        hint: 'It is in present-day Bihar.',
        options: ['Rajagriha', 'Pataliputra', 'Vaishali', 'Ujjain'],
        correctAnswer: 'Vaishali',
        explanation: 'Vaishali was the capital of the Vajji confederacy.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Ashvamedha', back: 'Horse sacrifice ritual to establish power'),
      Flashcard(front: 'Bhaga', back: 'Tax on crops (1/6th of produce)')
    ],
    revisionNotes: 'Magadha became powerful due to rivers, iron mines, and elephants.',
    commonMistakes: ['Confusing Magadha with Vajji systems']
  ),

  'ss6_h6': const ConceptNode(
    id: 'ss6_h6',
    subject: 'History',
    classLevel: 6,
    chapter: 'New Questions and Ideas',
    topic: 'Religion and Philosophy',
    subtopic: 'Buddhism, Jainism and Upanishads',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Story of Buddha and basic teachings',
      'Principles of Jainism (Lord Mahavira)',
      'Concepts of Atman and Brahman in Upanishads'
    ],
    examples: ['Story of Kisagotami', 'Sarnath (first sermon)'],
    misconceptions: ['Buddhism and Jainism were only for the rich'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where did the Buddha attain enlightenment?',
        hint: 'Under a Peepal tree.',
        options: ['Lumbini', 'Sarnath', 'Bodh Gaya', 'Kushinagar'],
        correctAnswer: 'Bodh Gaya',
        explanation: 'Siddhartha Gautama became the Buddha at Bodh Gaya in Bihar.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Tanha', back: 'Desire or craving (Buddhism)'),
      Flashcard(front: 'Sangha', back: 'Association of those who left their homes')
    ],
    revisionNotes: 'Ahimsa (non-violence) is a core value of Jainism.',
    commonMistakes: ['Confusing the birth place of Buddha with the enlightenment place']
  ),

  'ss6_h7': const ConceptNode(
    id: 'ss6_h7',
    subject: 'History',
    classLevel: 6,
    chapter: 'Ashoka, The Emperor Who Gave Up War',
    topic: 'Mauryan Empire',
    subtopic: 'Ashoka and Dhamma',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.evaluate,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: ['ss6_h5'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Founding of Mauryan Empire (Chandragupta Maurya)',
      'Impact of the Kalinga War',
      'Ashoka\'s Dhamma and its propagation'
    ],
    examples: ['Edicts of Ashoka', 'Lion Capital at Sarnath'],
    misconceptions: ['Dhamma is a new religion (it is a code of conduct)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which war changed Ashoka\'s heart?',
        hint: 'A bloody battle on the east coast.',
        options: ['Battle of Panipat', 'Kalinga War', 'Battle of Plassey', 'Magadha War'],
        correctAnswer: 'Kalinga War',
        explanation: 'The suffering in Kalinga made Ashoka embrace peace and Dhamma.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Chanakya', back: 'Wise man who wrote Arthashastra'),
      Flashcard(front: 'Pataliputra', back: 'Capital of the Mauryan Empire')
    ],
    revisionNotes: 'Ashoka was the first ruler to communicate with people through edicts.',
    commonMistakes: ['Thinking Ashoka was the founder of the empire']
  ),

  'ss6_h8': const ConceptNode(
    id: 'ss6_h8',
    subject: 'History',
    classLevel: 6,
    chapter: 'Vital Villages, Thriving Towns',
    topic: 'Ancient Economy',
    subtopic: 'Iron Tools and Trade',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Use of iron tools in agriculture',
      'Life in villages (Gramabhojaka, Grihapatis)',
      'Punch-marked coins and early trade centers (Arikamedu)'
    ],
    examples: ['Ring wells', 'Northern Black Polished Ware (NBPW)'],
    misconceptions: ['Cities didn\'t have sanitation (Ring wells were used for toilets/drains)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What were early coins called?',
        hint: 'Designs were hit onto the metal.',
        options: ['Gold coins', 'Punch-marked coins', 'Rupees', 'Dinars'],
        correctAnswer: 'Punch-marked coins',
        explanation: 'They were generally rectangular or round with symbols punched on them.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Gramabhojaka', back: 'Village headman (North India)'),
      Flashcard(front: 'Shrenis', back: 'Associations of crafts persons and merchants')
    ],
    revisionNotes: 'Irrigation (canals, wells, tanks) boosted production.',
    commonMistakes: ['Thinking everyone in villages owned land']
  ),

  'ss6_h9': const ConceptNode(
    id: 'ss6_h9',
    subject: 'History',
    classLevel: 6,
    chapter: 'Traders, Kings and Pilgrims',
    topic: 'Ancient Trade',
    subtopic: 'Silk Route and Bhakti',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'The famous Silk Route and its control',
      'Spread of Buddhism (Mahayana) and statues',
      'Rise of Bhakti and foreign pilgrims (Fa-Xian, Xuan Zang)'
    ],
    examples: ['Kushanas and Kanishka', 'Nalanda university'],
    misconceptions: ['The Silk Route was only for silk'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which famous university did Xuan Zang visit in India?',
        hint: 'A great center of learning.',
        options: ['Taxila', 'Nalanda', 'Vikramshila', 'Banaras'],
        correctAnswer: 'Nalanda',
        explanation: 'Nalanda was a world-famous Buddhist monastery and university.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Bhakti', back: 'Devotion to a chosen deity'),
      Flashcard(front: 'Bodhisattvas', back: 'Enlightened persons who stayed to help others')
    ],
    revisionNotes: 'Trade spread not just goods, but also ideas and religions.',
    commonMistakes: ['Thinking Buddhism didn\'t change over time']
  ),

  'ss6_h10': const ConceptNode(
    id: 'ss6_h10',
    subject: 'History',
    classLevel: 6,
    chapter: 'New Empires and Kingdoms',
    topic: 'Political History',
    subtopic: 'Guptas, Pallavas and Chalukyas',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Learn about Samudragupta from Prashastis',
      'The Golden Age of Guptas (Harshavardhana)',
      'Kingdoms in the South (Pallavas and Chalukyas)'
    ],
    examples: ['Allahabad Pillar inscription', 'Aihole inscription'],
    misconceptions: ['Southern kingdoms were less organized than Northern ones'],
    practiceExercises: [
      PracticeExercise(
        question: 'Who was the court poet of Samudragupta?',
        hint: 'He wrote the Allahabad Prashasti.',
        options: ['Kalidasa', 'Harishena', 'Banabhatta', 'Ravikirti'],
        correctAnswer: 'Harishena',
        explanation: 'Harishena wrote a long poem in praise of Samudragupta.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Prashasti', back: 'Sanskrit word meaning "in praise of"'),
      Flashcard(front: 'Dakshinapatha', back: 'Route to the south (12 rulers defeated by Samudragupta)')
    ],
    revisionNotes: 'Administrative systems became more decentralized during this period.',
    commonMistakes: ['Confusing Harishena with Ravikirti (Chalukya poet)']
  ),

  'ss6_h11': const ConceptNode(
    id: 'ss6_h11',
    subject: 'History',
    classLevel: 6,
    chapter: 'Buildings, Paintings and Books',
    topic: 'Culture and Art',
    subtopic: 'Iron Pillar, Stupas and Epics',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.remember,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Metallurgy (Iron Pillar at Mehrauli)',
      'Architecture of Stupas and Temples',
      'Literature: Epics (Silappadikaram, Ramayana, Mahabharata)'
    ],
    examples: ['Ajanta paintings', 'Aryabhatiyam by Aryabhata'],
    misconceptions: ['Ancient Indians didn\'t know advanced science (Aryabhata knew Earth rotates!)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Where is the famous Iron Pillar located?',
        hint: 'Near the Qutub Minar in Delhi.',
        options: ['Delhi', 'Mumbai', 'Agra', 'Patna'],
        correctAnswer: 'Delhi',
        explanation: 'The Iron Pillar at Mehrauli, Delhi, hasn\'t rusted in 1500 years!'
      )
    ],
    flashcards: [
      Flashcard(front: 'Aryabhata', back: 'Mathematician and Astronomer who explained eclipses'),
      Flashcard(front: 'Stupa', back: 'Relic casket (mound) containing Buddhist remains')
    ],
    revisionNotes: 'Stories were preserved through Puranas and Epics.',
    commonMistakes: ['Thinking temples and stupas were built by one person alone']
  ),

  // ===========================================================================
  // CLASS 6 SOCIAL SCIENCE (Geography - The Earth: Our Habitat)
  // ===========================================================================

  'ss6_g1': const ConceptNode(
    id: 'ss6_g1',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'The Earth in the Solar System',
    topic: 'Astronomy',
    subtopic: 'Celestial Bodies',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.remember,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: ['e5_c11'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Define celestial bodies: Stars, Planets, Satellites',
      'Understand the Solar System components',
      'Unique features of Earth and Moon'
    ],
    examples: ['Sun is a star', 'Earth is the Blue Planet'],
    misconceptions: ['Stars are small (they are huge but very far away)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which is the third nearest planet to the Sun?',
        hint: 'It is our home.',
        options: ['Venus', 'Mars', 'Earth', 'Jupiter'],
        correctAnswer: 'Earth',
        explanation: 'The order is Mercury, Venus, Earth...'
      )
    ],
    flashcards: [
      Flashcard(front: 'Galaxy', back: 'Huge system of billions of stars (e.g. Milky Way)'),
      Flashcard(front: 'Orbit', back: 'Fixed path on which planets move around Sun')
    ],
    revisionNotes: 'Earth is the only planet known to have life.',
    commonMistakes: ['Thinking Pluto is still a planet (it is a dwarf planet)']
  ),

  'ss6_g2': const ConceptNode(
    id: 'ss6_g2',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'Globe: Latitudes and Longitudes',
    topic: 'Cartography',
    subtopic: 'Grid System and Time',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Define Equator, Parallels of Latitudes',
      'Understand Meridians of Longitudes and Prime Meridian',
      'Relationship between Longitude and Time'
    ],
    examples: ['IST (Indian Standard Time) is 82°30\'E', 'Equator is 0° latitude'],
    misconceptions: ['Latitudes meet at the poles (Longitudes meet at poles, latitudes are parallel)'],
    practiceExercises: [
      PracticeExercise(
        question: 'What is the value of the Prime Meridian?',
        hint: 'It passes through Greenwich.',
        options: ['90°', '0°', '180°', '60°'],
        correctAnswer: '0°',
        explanation: 'Prime Meridian is the starting point for Longitude.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Torrid Zone', back: 'Hottest zone between Tropics'),
      Flashcard(front: 'Grid', back: 'Network of latitudes and longitudes')
    ],
    revisionNotes: '1 degree of longitude = 4 minutes of time.',
    commonMistakes: ['Confusing Latitudes with Longitudes']
  ),

  'ss6_g3': const ConceptNode(
    id: 'ss6_g3',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'Motions of the Earth',
    topic: 'Astronomy',
    subtopic: 'Rotation and Revolution',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 45),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Difference between Rotation and Revolution',
      'Causes of Day and Night',
      'Causes of Seasons (Solstice and Equinox)'
    ],
    examples: ['Leap year every 4 years', 'Christmas in summer in Australia'],
    misconceptions: ['Seasons are caused by Earth being closer to Sun (it is caused by the TILT of the axis)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Motion of the earth around the sun is called?',
        hint: 'It takes 365 days.',
        options: ['Rotation', 'Revolution', 'Orbital Plane', 'Circle of Illumination'],
        correctAnswer: 'Revolution',
        explanation: 'Revolution is the movement in a fixed path around the Sun.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Equinox', back: 'Days when whole earth has equal day and night (Mar 21, Sept 23)'),
      Flashcard(front: 'Rotation', back: 'Movement of earth on its axis (takes 24h)')
    ],
    revisionNotes: 'Earth\'s axis is tilted at 66.5 degrees to its orbital plane.',
    commonMistakes: ['Forgetting the tilt while explaining seasons']
  ),

  'ss6_g4': const ConceptNode(
    id: 'ss6_g4',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'Maps',
    topic: 'Cartography',
    subtopic: 'Types and Components',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 5,
    estStudyTime: const Duration(minutes: 35),
    prerequisites: ['m5_c8'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Difference between Map and Globe',
      'Components: Distance (Scale), Direction, Symbol',
      'Types: Physical, Political, Thematic'
    ],
    examples: ['Thematic map for rainfall', 'Compass Rose for directions'],
    misconceptions: ['A Sketch is as accurate as a Map'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which map shows distribution of forests?',
        hint: 'It is a specific theme.',
        options: ['Physical', 'Political', 'Thematic', 'Globe'],
        correctAnswer: 'Thematic',
        explanation: 'Thematic maps focus on specific information like weather, roads, or industries.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Cardinal Points', back: 'North, South, East, West'),
      Flashcard(front: 'Plan', back: 'Drawing of a small area on a large scale')
    ],
    revisionNotes: 'Blue color represents water, Brown for mountains, Green for plains.',
    commonMistakes: ['Using wrong scale for small area maps']
  ),

  'ss6_g5': const ConceptNode(
    id: 'ss6_g5',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'Major Domains of the Earth',
    topic: 'Physical Geography',
    subtopic: 'Spheres of the Earth',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 8,
    estStudyTime: const Duration(minutes: 50),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Define Lithosphere, Atmosphere, Hydrosphere, Biosphere',
      'Names and features of 7 Continents',
      'Names and features of 5 Oceans'
    ],
    examples: ['Mt. Everest is the highest peak', 'Mariana Trench is the deepest point'],
    misconceptions: ['Atmosphere is only Oxygen (it is a mixture)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which is the largest continent?',
        hint: 'India is part of it.',
        options: ['Africa', 'Asia', 'North America', 'Europe'],
        correctAnswer: 'Asia',
        explanation: 'Asia covers about one-third of the total land area of the earth.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Biosphere', back: 'Narrow zone where land, water, and air meet'),
      Flashcard(front: 'Isthmus', back: 'Narrow strip of land joining two landmasses')
    ],
    revisionNotes: '97% of Earth\'s water is in oceans and is too salty for use.',
    commonMistakes: ['Confusing Isthmus with Strait']
  ),

  'ss6_g6': const ConceptNode(
    id: 'ss6_g6',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'Major Landforms of the Earth',
    topic: 'Physical Geography',
    subtopic: 'Mountains, Plateaus and Plains',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.understand,
    examWeightage: 6,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Types of Mountains (Fold, Block, Volcanic)',
      'Features of Plateaus (Deccan, Tibet)',
      'Importance of Plains for human settlement'
    ],
    examples: ['Himalayas (Fold)', 'Vindhyas (Block)', 'Kilimanjaro (Volcanic)'],
    misconceptions: ['All high lands are mountains (Plateaus are high but flat)'],
    practiceExercises: [
      PracticeExercise(
        question: 'Which landform is very rich in mineral deposits?',
        hint: 'It is a table-land.',
        options: ['Mountains', 'Plateaus', 'Plains', 'Valleys'],
        correctAnswer: 'Plateaus',
        explanation: 'Plateaus like the Deccan or Chhotanagpur are famous for minerals.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Glacier', back: 'Permanently frozen rivers of ice'),
      Flashcard(front: 'Erosion', back: 'Wearing away of the earth\'s surface')
    ],
    revisionNotes: 'Plains are formed by rivers and are most fertile.',
    commonMistakes: ['Thinking mountains are only found in cold places']
  ),

  'ss6_g7': const ConceptNode(
    id: 'ss6_g7',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'Our Country - India',
    topic: 'Regional Geography',
    subtopic: 'Location and Physical Divisions',
    difficulty: Difficulty.intermediate,
    bloomLevel: BloomLevel.apply,
    examWeightage: 9,
    estStudyTime: const Duration(minutes: 55),
    prerequisites: ['ss6_g2'],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Locational setting (Hemispheres, IST)',
      'Neighbors of India and Political divisions',
      'Physical divisions: Himalayas, Northern Plains, Peninsular Plateau, Islands'
    ],
    examples: ['Tropic of Cancer passes through middle', 'Lakshadweep are Coral islands'],
    misconceptions: ['Sri Lanka is connected to India by land'],
    practiceExercises: [
      PracticeExercise(
        question: 'The southernmost part of India is?',
        hint: 'It starts with K.',
        options: ['Kashmir', 'Kanyakumari', 'Kerala', 'Kolkata'],
        correctAnswer: 'Kanyakumari',
        explanation: 'Kanyakumari is the southern tip of the mainland.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Himadri', back: 'The Great Himalayas / Northernmost range'),
      Flashcard(front: 'Delta', back: 'Triangular land formed at the mouth of a river')
    ],
    revisionNotes: 'India is the 7th largest country in the world.',
    commonMistakes: ['Confusing Arabian Sea with Bay of Bengal location']
  ),

  'ss6_g8': const ConceptNode(
    id: 'ss6_g8',
    subject: 'Geography',
    classLevel: 6,
    chapter: 'India: Climate, Vegetation and Wildlife',
    topic: 'Environmental Geography',
    subtopic: 'Weather and Life',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.understand,
    examWeightage: 7,
    estStudyTime: const Duration(minutes: 40),
    prerequisites: [],
    dependencies: [],
    relatedConcepts: [],
    learningObjectives: [
      'Major seasons in India (Winter, Summer, Monsoon)',
      'Natural Vegetation: Tropical Evergreen, Deciduous, Thorny',
      'Importance of Forests and Wildlife conservation'
    ],
    examples: ['Gir forest (Lions)', 'Sundarbans (Tigers)'],
    misconceptions: ['Weather and Climate are the same (Weather is day-to-day, Climate is long-term)'],
    practiceExercises: [
      PracticeExercise(
        question: 'During which season does the "Loo" wind blow?',
        hint: 'It is very hot.',
        options: ['Winter', 'Monsoon', 'Summer', 'Autumn'],
        correctAnswer: 'Summer',
        explanation: 'Hot and dry winds called Loo blow during the day in summer.'
      )
    ],
    flashcards: [
      Flashcard(front: 'Mawsynram', back: 'Place in Meghalaya with highest rainfall in world'),
      Flashcard(front: 'Van Mahotsav', back: 'Festival of planting trees')
    ],
    revisionNotes: 'Monsoon is the most important season for Indian agriculture.',
    commonMistakes: ['Thinking all forests stay green all year']
  )
};
