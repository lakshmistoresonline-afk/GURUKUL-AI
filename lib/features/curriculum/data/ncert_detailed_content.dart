import '../domain/models/concept_node.dart';

final Map<String, ConceptNode> ncertDetailedContent = {
  // ===========================================================================
  // CLASS 5 MATHEMATICS (Math-Magic)
  // ===========================================================================

  'm5_c1': ConceptNode(
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
        options: const ['5', '6', '7', '8'],
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
    introduction: 'Welcome to the world of big catches! In "The Fish Tale", we dive into the ocean to learn about large numbers through the story of a busy fish market.',
    realLifeConnection: 'Large numbers are used to talk about the population of a country, the cost of a plane, or how many stars are in a galaxy!',
    storyBasedExplanation: 'Imagine Meena the fisherwoman. She caught so many fish that her small scale couldn\'t weigh them! She needed to count them in Lakhs. Her teacher told her that 100 thousands make 1 Lakh.',
    childFriendlyExplanation: 'Think of numbers like a growing family. First, we have the small ones, then thousands, then the big grandparents: Lakhs and Crores!',
    teacherExplanation: 'Numeration in the Indian system follows a 3-2-2 comma pattern. The periods are Ones, Thousands, Lakhs, and Crores.',
    animatedLessonAsset: 'assets/lottie/math_numbers.json',
    handsOnActivities: const [
      'Find 5 large numbers in a newspaper and write them in words.',
      'Create a "Place Value House" using cardboard for Lakhs and Crores.'
    ],
    masteryCheckpoints: const [
      'Can correctly place commas in a 7-digit number.',
      'Can compare two numbers in the lakhs range.',
      'Understands the relationship between Lakh and Million.'
    ]
  ),

  'm5_c2': ConceptNode(
    id: 'm5_c2',
    subject: 'Mathematics',
    classLevel: 5,
    chapter: 'Shapes and Angles',
    topic: 'Geometry',
    subtopic: 'Types of Angles',
    difficulty: Difficulty.beginner,
    bloomLevel: BloomLevel.apply,
    examWeightage: 7,
    estStudyTime: Duration(minutes: 40),
    prerequisites: const [],
    dependencies: const ['m6_c4'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify Right, Acute, and Obtuse angles',
      'Recognize angles in daily life objects',
      'Understand how shapes change with angles'
    ],
    examples: const ['Corner of a book (Right angle)', 'Hands of a clock at 3:00'],
    misconceptions: const ['Thinking bigger shapes have bigger angles'],
    practiceExercises: const [
      PracticeExercise(
        question: 'An angle smaller than a right angle is called?',
        hint: 'It is a "sharp" angle.',
        options: const ['Obtuse', 'Right', 'Acute', 'Straight'],
        correctAnswer: 'Acute',
        explanation: 'Acute angles are less than 90 degrees.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Right Angle', back: '90 degrees (L shape)'),
      Flashcard(front: 'Obtuse Angle', back: 'More than 90, less than 180')
    ],
    revisionNotes: 'Use a "Degree Clock" or Divider to measure angles.',
    commonMistakes: const ['Confusing Acute and Obtuse'],
    vocabulary: const {
      'Acute Angle': 'An angle that is less than 90 degrees.',
      'Obtuse Angle': 'An angle that is greater than 90 degrees but less than 180 degrees.',
      'Right Angle': 'An angle of exactly 90 degrees.'
    },
    introduction: 'Look around you! Everything has an angle. From the yoga poses you do to the roof of your house.',
    realLifeConnection: 'When you open a door just a little bit, you make an acute angle. Open it wide, and it becomes obtuse!',
    storyBasedExplanation: 'Rohini and Mohini are making shapes with matchsticks. They noticed that by changing the angle, the whole shape changes from a square to a rhombus!',
    childFriendlyExplanation: 'Angles are like the mouths of hungry crocodiles. A small opening is Acute, a perfect "L" is Right, and a wide open mouth is Obtuse!',
    teacherExplanation: 'An angle is formed when two rays meet at a common vertex. We measure them in degrees using a protractor.',
    animatedLessonAsset: 'assets/lottie/geometry_angles.json',
    handsOnActivities: const [
      'Make an "Angle Tester" using two strips of cardboard and a split pin.',
      'Find 3 right angles in your kitchen.'
    ],
    interactiveActivities: const [
      'Look around your room and find 5 objects that have a right angle.',
      'Use two pencils to show an angle that is "more than a right angle".'
    ],
    masteryCheckpoints: const [
      'Identifies right angles in 2D shapes.',
      'Distinguishes between sharp (acute) and wide (obtuse) corners.',
      'Can use a degree clock to represent a half-right angle.'
    ]
  ),

  'm5_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['m5_c11', 'm6_c10'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Calculate area by counting squares',
      'Understand perimeter as boundary length',
      'Compare areas of different shapes'
    ],
    examples: const ['Area of a stamp on a grid', 'Perimeter of a rectangular field'],
    misconceptions: const ['Thinking shapes with same area must have same perimeter'],
    practiceExercises: const [
      PracticeExercise(
        question: 'If a square has side 3cm, what is its area?',
        hint: 'Count the 1x1 squares inside.',
        options: const ['6 sq cm', '9 sq cm', '12 sq cm', '3 sq cm'],
        correctAnswer: '9 sq cm',
        explanation: 'Area of square = side x side = 3 x 3 = 9.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Area', back: 'Space inside a boundary'),
      Flashcard(front: 'Perimeter', back: 'Length of the boundary')
    ],
    revisionNotes: 'Perimeter is sum of all sides. Area is measured in square units.',
    commonMistakes: const ['Confusing formulas for area and perimeter'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c4': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['m6_c7'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand numerator and denominator',
      'Equivalent fractions',
      'Represent fractions on a grid or flag'
    ],
    examples: const ['Half an apple (1/2)', 'Three-fourths of a pizza (3/4)'],
    misconceptions: const ['Thinking 1/4 is bigger than 1/2 because 4 > 2'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which is an equivalent fraction of 1/2?',
        hint: 'Multiply numerator and denominator by 2.',
        options: const ['1/4', '2/4', '1/3', '2/3'],
        correctAnswer: '2/4',
        explanation: '1/2 = (1*2)/(2*2) = 2/4.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Numerator', back: 'Number of parts we have'),
      Flashcard(front: 'Denominator', back: 'Total number of equal parts')
    ],
    revisionNotes: 'Equivalent fractions represent the same amount.',
    commonMistakes: const ['Comparing denominators directly without common base'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c5': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Mirror halves and symmetry lines',
      'Half-turn and quarter-turn rotations',
      'Patterns in rotational symmetry'
    ],
    examples: const ['Letter H (vertical symmetry)', 'A fan (rotational symmetry)'],
    misconceptions: const ['Thinking every shape has a mirror half'],
    practiceExercises: const [
      PracticeExercise(
        question: 'If you give a half-turn to the letter "S", does it look the same?',
        hint: 'Rotate your phone upside down.',
        options: const ['Yes', 'No'],
        correctAnswer: 'Yes',
        explanation: '"S" looks the same after a 180-degree (half) turn.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Line of Symmetry', back: 'Line that divides a shape into mirror halves'),
      Flashcard(front: 'Half Turn', back: '180 degree rotation')
    ],
    revisionNotes: 'Symmetry is found in nature, letters, and art.',
    commonMistakes: const ['Incorrectly identifying lines of symmetry in non-regular shapes'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c6': ConceptNode(
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
    prerequisites: const ['m5_c1'],
    dependencies: const ['m6_c3'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Find multiples of a number',
      'Identify common multiples and LCM',
      'Find factors and HCF'
    ],
    examples: const ['Multiples of 3: 3, 6, 9...', 'Factors of 6: 1, 2, 3, 6'],
    misconceptions: const ['Confusing factors with multiples'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the smallest common multiple of 4 and 6?',
        hint: 'List them: 4, 8, 12... and 6, 12...',
        options: const ['2', '12', '24', '1'],
        correctAnswer: '12',
        explanation: 'Multiples of 4: 4, 8, 12, 16... Multiples of 6: 6, 12, 18... Smallest common is 12.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Multiple', back: 'Number obtained by multiplying with 1, 2, 3...'),
      Flashcard(front: 'Factor', back: 'Number that divides exactly without remainder')
    ],
    revisionNotes: 'Every number is a factor and multiple of itself. 1 is a factor of every number.',
    commonMistakes: const ['Thinking factors are infinite (multiples are infinite)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c7': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify number patterns',
      'Create and solve magic squares',
      'Understand rules of rotation in patterns'
    ],
    examples: const ['1, 3, 6, 10 (Triangular numbers)', 'Magic Square where all sides sum to 150'],
    misconceptions: const ['Patterns only exist in numbers (they exist in shapes too)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'In a magic square, the sum of rows, columns, and diagonals is?',
        hint: 'It is always the same.',
        options: const ['Different', 'Zero', 'The Same', 'Random'],
        correctAnswer: 'The Same',
        explanation: 'That is what makes it "Magic"!'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Palindromes', back: 'Numbers that read the same forwards and backwards (e.g., 121)')
    ],
    revisionNotes: 'Look for the "rule" in every pattern.',
    commonMistakes: const ['Incomplete rows in magic squares'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['m6_g4'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Read maps and identify landmarks',
      'Understand scale (e.g., 1cm = 200km)',
      'Find routes and directions'
    ],
    examples: const ['Map of India', 'Route from school to home'],
    misconceptions: const ['Thinking distance on map is same as real distance'],
    practiceExercises: const [
      PracticeExercise(
        question: 'If scale is 1cm = 10km, how far is 5cm on the map in reality?',
        hint: 'Multiply 5 by 10.',
        options: const ['15 km', '50 km', '5 km', '500 km'],
        correctAnswer: '50 km',
        explanation: '5 * 10km = 50km.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Scale', back: 'Ratio of distance on map to real distance')
    ],
    revisionNotes: 'Maps help us find our way. Scaling up or down changes size but not shape.',
    commonMistakes: const ['Using wrong multiplication for scale conversion'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c9': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['m6_c5'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify 3D shapes (Cube, Cylinder, Cone)',
      'Draw floor maps and deep drawings',
      'Understand "Nets" that fold into boxes'
    ],
    examples: const ['A dice (Cube)', 'A birthday cap (Cone)'],
    misconceptions: const ['Thinking all 2D drawings are "Deep Drawings"'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which of these folds into a cube?',
        hint: 'A cube has 6 square faces.',
        options: const ['A T-shaped net with 6 squares', 'A triangle', 'A circle', 'A 5-square net'],
        correctAnswer: 'A T-shaped net with 6 squares',
        explanation: 'A cube needs exactly 6 faces to be complete.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Net', back: '2D shape that can be folded into a 3D box')
    ],
    revisionNotes: 'Nets are like the "clothes" of a 3D shape.',
    commonMistakes: const ['Missing faces in a net'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c10': ConceptNode(
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
    prerequisites: const ['m5_c4'],
    dependencies: const ['m6_c8'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Represent fractions as decimals',
      'Understand tenths (0.1) and hundredths (0.01)',
      'Apply decimals in currency and length'
    ],
    examples: const ['10 paise = 0.10 rupee', 'Length of a pencil: 15.5 cm'],
    misconceptions: const ['Thinking 0.11 is bigger than 0.2 (0.2 is actually 0.20)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Write 5/100 as a decimal.',
        hint: 'It is five-hundredths.',
        options: const ['0.5', '0.05', '5.0', '0.005'],
        correctAnswer: '0.05',
        explanation: 'Division by 100 moves the decimal two places left.'
      )
    ],
    flashcards: const [
      Flashcard(front: '1 Tenth', back: '1/10 or 0.1'),
      Flashcard(front: '1 Hundredth', back: '1/100 or 0.01')
    ],
    revisionNotes: 'Decimal point separates the whole number from the fractional part.',
    commonMistakes: const ['Incorrect zero placement after decimal'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c11': ConceptNode(
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
    prerequisites: const ['m5_c3'],
    dependencies: const ['m6_c10'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Calculate area of large fields',
      'Word problems on perimeter',
      'Find missing sides given area/perimeter'
    ],
    examples: const ['Fencing a garden', 'Dividing a plot into smaller squares'],
    misconceptions: const ['Confusing L+B with 2*(L+B)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'If perimeter is 20cm and length is 6cm, what is breadth?',
        hint: 'Perimeter = 2*(L+B). So L+B = 10.',
        options: const ['4 cm', '14 cm', '10 cm', '2 cm'],
        correctAnswer: '4 cm',
        explanation: '2*(6+B)=20 -> 6+B=10 -> B=4.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Rectangle Area', back: 'Length x Breadth'),
      Flashcard(front: 'Rectangle Perimeter', back: '2 * (Length + Breadth)')
    ],
    revisionNotes: 'Always check the units (cm vs m).',
    commonMistakes: const ['Forgetting to multiply by 2 in perimeter'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c12': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['m6_c9'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Organize data using Tally Marks',
      'Interpret Bar Graphs and Pie Charts',
      'Growth charts for plants/animals'
    ],
    examples: const ['Recording favorite colors of students', 'Rainfall over 5 months'],
    misconceptions: const ['Thinking tally marks can only go up to 5'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What does a full block of 4 lines with a cross represent in Tally?',
        hint: 'Count the lines.',
        options: const ['4', '5', '6', '10'],
        correctAnswer: '5',
        explanation: 'Four vertical lines and one diagonal across them is the standard for 5.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Pie Chart', back: 'Circular chart representing data as parts of a whole')
    ],
    revisionNotes: 'Charts make data easy to understand at a glance.',
    commonMistakes: const ['Misreading the scale of a Bar Graph'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c13': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Multiply using box method and standard method',
      'Solve division problems with remainders',
      'Unitary method in daily life'
    ],
    examples: const ['Salary calculation', 'Cost of 12 eggs if 1 is 5 rupees'],
    misconceptions: const ['Remainder can be bigger than divisor'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Divide 450 by 9.',
        hint: '9 times what is 45?',
        options: const ['5', '50', '55', '45'],
        correctAnswer: '50',
        explanation: '45/9 = 5, so 450/9 = 50.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Divisor', back: 'The number we divide by'),
      Flashcard(front: 'Quotient', back: 'The result of division')
    ],
    revisionNotes: 'Check division: (Divisor * Quotient) + Remainder = Dividend.',
    commonMistakes: const ['Calculation errors in long multiplication'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm5_c14': ConceptNode(
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
    prerequisites: const ['m5_c11'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand volume as space occupied',
      'Measure volume of cubes/cuboids',
      'Relationship between volume and water displacement'
    ],
    examples: const ['Volume of a box of matchboxes', 'Weight of a coin collection'],
    misconceptions: const ['Heavier objects always have more volume'],
    practiceExercises: const [
      PracticeExercise(
        question: 'If a cube has side 2cm, what is its volume?',
        hint: 'Volume = side x side x side.',
        options: const ['4 cu cm', '6 cu cm', '8 cu cm', '2 cu cm'],
        correctAnswer: '8 cu cm',
        explanation: '2 x 2 x 2 = 8.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Volume', back: 'Space occupied by a 3D object'),
      Flashcard(front: '1 Litre', back: '1000 millilitres')
    ],
    revisionNotes: 'Volume is 3D (L x B x H). Weight is measured in grams and kilograms.',
    commonMistakes: const ['Confusing Area (sq) with Volume (cu)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 5 EVS (Looking Around)
  // ===========================================================================

  'e5_c1': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['s6_c5'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Describe special senses of animals',
      'Understand how animals communicate',
      'Awareness of tiger conservation'
    ],
    examples: const ['Eagles can see 4 times as far as humans', 'Tigers can move their ears to catch sound'],
    misconceptions: const ['Animals sleep exactly like humans'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which bird has eyes in front of its head (like humans)?',
        hint: 'It is an nocturnal bird.',
        options: const ['Eagle', 'Sparrow', 'Owl', 'Parrot'],
        correctAnswer: 'Owl',
        explanation: 'Owls have eyes in the front of their face, unlike most birds.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Sloth Sleep Time', back: '17 hours a day'),
      Flashcard(front: 'Tiger Roar Distance', back: 'Can be heard 3km away')
    ],
    revisionNotes: 'Focus on Sloth, Tiger, and senses of Ants/Dogs.',
    commonMistakes: const ['Thinking all animals see color (most see fewer colors than us)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c2': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about Kalbeliya community',
      'Understand relationship between humans and animals',
      'Laws regarding wildlife protection'
    ],
    examples: const ['Been dance', 'Nagmumphan patterns'],
    misconceptions: const ['All snakes are poisonous (only a few are)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which community is famous for snake charming?',
        hint: 'They have a special dance too.',
        options: const ['Gonds', 'Kalbeliyas', 'Bheels', 'Santhals'],
        correctAnswer: 'Kalbeliyas',
        explanation: 'Kalbeliyas are a community that used to catch snakes and entertain people.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Poisonous snakes in India', back: 'Cobra, Common Krait, Russel’s Viper, Saw-scaled Viper')
    ],
    revisionNotes: 'Snake charmers help villagers during snake bites and treat snakes as treasures.',
    commonMistakes: const ['Thinking snake charmers harm snakes (mostly they care for them)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['s6_c1'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify different taste zones on the tongue',
      'Understand the process of digestion',
      'Importance of a balanced diet and glucose'
    ],
    examples: const ['Saliva starting digestion', 'Glucose drip for energy'],
    misconceptions: const ['Digestion only happens in the stomach'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the liquid in our mouth that helps in digestion?',
        hint: 'It makes food soft.',
        options: const ['Water', 'Acid', 'Saliva', 'Blood'],
        correctAnswer: 'Saliva',
        explanation: 'Saliva breaks down food and makes it easy to swallow.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Stomach Temperature', back: 'About 30°C'),
      Flashcard(front: 'Dr. Beaumont', back: 'Doctor who studied digestion through a hole in a stomach')
    ],
    revisionNotes: 'Chew food well for better digestion. Digestion ends in the intestines.',
    commonMistakes: const ['Swallowing food too fast'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c4': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn how food gets spoiled',
      'Techniques for preserving food (Drying, Salting, Sugaring)',
      'Story of Mamidi Tandra (Aam Papad)'
    ],
    examples: const ['Pickling', 'Refrigeration', 'Milk pasteurization'],
    misconceptions: const ['Cooked food never spoils'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is Mamidi Tandra made from?',
        hint: 'It is a king of fruits.',
        options: const ['Apple', 'Mango', 'Banana', 'Orange'],
        correctAnswer: 'Mango',
        explanation: 'Mamidi Tandra is the Telugu name for Aam Papad, made from mango pulp.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Preserving Milk', back: 'Boil it'),
      Flashcard(front: 'Preserving Onions', back: 'Keep in dry open place')
    ],
    revisionNotes: 'Check expiry dates on food packets. Glass jars should be dried before pickling.',
    commonMistakes: const ['Using wet spoons in pickle jars'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c5': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['s6_c4'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Conditions required for germination',
      'Methods of seed dispersal (Wind, Water, Animals)',
      'Insectivorous plants (Pitcher plant)'
    ],
    examples: const ['Dandelion seeds flying', 'Velcro invented from seeds'],
    misconceptions: const ['Seeds need only water to grow (they need air and warmth too)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which plant traps and eats insects?',
        hint: 'It is shaped like a jug.',
        options: const ['Cactus', 'Pitcher Plant', 'Rose', 'Peepal'],
        correctAnswer: 'Pitcher Plant',
        explanation: 'Nepenthes (Pitcher plant) traps insects to get nitrogen.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Dispersal by Air', back: 'Light seeds with hair (e.g. Cotton)'),
      Flashcard(front: 'Dispersal by Animals', back: 'Hooks or sticking to fur')
    ],
    revisionNotes: 'Seeds are "sleeping" plants. Sprouted grains are very healthy.',
    commonMistakes: const ['Soaking seeds for too long without air'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Historical water systems (Ghadisar, Stepwells)',
      'Methods of rainwater harvesting',
      'Importance of water for survival'
    ],
    examples: const ['Bawris (Stepwells)', 'Rainwater harvesting in Rajasthan'],
    misconceptions: const ['Groundwater is infinite'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is a "Bawri"?',
        hint: 'It has steps going down.',
        options: const ['A Lake', 'A Stepwell', 'A River', 'A Dam'],
        correctAnswer: 'A Stepwell',
        explanation: 'Stepwells (Bawris) are old systems where steps go deep to reach water.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Al-Biruni', back: 'Traveller from Uzbekistan who wrote about Indian ponds'),
      Flashcard(front: 'Tarun Bharat Sangh', back: 'Group that helps rebuild old lakes')
    ],
    revisionNotes: 'Save water today for a better tomorrow. Reuse water where possible.',
    commonMistakes: const ['Leaving taps running'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c7': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['s6_c2'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand what floats and what sinks',
      'Soluble vs Insoluble substances',
      'Evaporation (Dandi March / Salt story)'
    ],
    examples: const ['Sugar dissolving in water', 'Oil floating on water'],
    misconceptions: const ['Heavy things always sink (a huge ship floats!)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why does a person float in the Dead Sea even if they can\'t swim?',
        hint: 'The water is very salty.',
        options: const ['Less salt', 'High salt content', 'Cold water', 'Deep water'],
        correctAnswer: 'High salt content',
        explanation: 'Very salty water makes it easy to float because the water becomes "heavy".'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Soluble', back: 'Mixes and disappears in water'),
      Flashcard(front: 'Dandi March', back: 'Mahatma Gandhi’s march in 1930 to protest salt law')
    ],
    revisionNotes: 'Stirring and heating help things dissolve faster.',
    commonMistakes: const ['Confusing floating with dissolving'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify symptoms of Malaria and Anemia',
      'Lifecycles of mosquitoes and flies',
      'Prevention of mosquito-borne diseases'
    ],
    examples: const ['Iron-rich food: Jaggery, Amla, Spinach', 'Mosquito nets'],
    misconceptions: const ['Mosquitoes spread Malaria through dirty water (they BREED in water, but bite humans)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which scientist discovered that mosquitoes spread malaria?',
        hint: 'He got a Nobel Prize.',
        options: const ['Louis Pasteur', 'Ronald Ross', 'Newton', 'Einstein'],
        correctAnswer: 'Ronald Ross',
        explanation: 'Ronald Ross discovered malaria parasites in the stomach of a mosquito.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Anemia', back: 'Low Hemoglobin or Iron in blood'),
      Flashcard(front: 'Larvae', back: 'Baby mosquitoes (look like threads)')
    ],
    revisionNotes: 'Do not let water collect around your house. Use oil to kill larvae in ponds.',
    commonMistakes: const ['Thinking flies spread malaria (they spread stomach infections)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c9': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Challenges of mountaineering',
      'Responsibilities of a group leader',
      'Bachendri Pal’s achievement'
    ],
    examples: const ['Rappelling', 'Sleeping bags', 'Nylon tents'],
    misconceptions: const ['Climbing mountains is only about strength (it is about mental grit too)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who was the first Indian woman to reach Mt. Everest?',
        hint: 'Her story is in the chapter.',
        options: const ['Sania Mirza', 'Bachendri Pal', 'P.V. Sindhu', 'Kalpana Chawla'],
        correctAnswer: 'Bachendri Pal',
        explanation: 'Bachendri Pal climbed Mt. Everest in 1984.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Rappelling', back: 'Coming down a mountain using a rope'),
      Flashcard(front: 'Vitamins for climbers', back: 'Vitamin C and Iron for strength/warmth')
    ],
    revisionNotes: 'Leadership means caring for the team and taking the lead when others are tired.',
    commonMistakes: const ['Thinking Everest is in India (it is in Nepal/Tibet)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c10': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['ss6_h3'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Architecture of Golconda Fort',
      'Old systems of water supply in forts',
      'Life in royal palaces vs common people'
    ],
    examples: const ['Bastions (Burj)', 'Cannons', 'Museums'],
    misconceptions: const ['Old buildings didn\'t have "modern" facilities like pipes'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What are the round parts of a fort wall called?',
        hint: 'They are higher than the wall.',
        options: const ['Gates', 'Bastions', 'Towers', 'Rooms'],
        correctAnswer: 'Bastions',
        explanation: 'Bastions (Burj) help soldiers see in all directions for safety.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Golconda Fort location', back: 'Hyderabad'),
      Flashcard(front: 'Cannon material', back: 'Bronze (mixture of copper and tin)')
    ],
    revisionNotes: 'Museums help us know how people lived, what they wore, and what they used.',
    commonMistakes: const ['Writing on monument walls'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c11': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['ss6_g1'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Concept of gravity and weightlessness',
      'How Earth looks from space',
      'Life of an astronaut'
    ],
    examples: const ['Floating food in space', 'Space shuttle'],
    misconceptions: const ['Space has no air (true), so people fall down (false, they float)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why do things fall towards the Earth?',
        hint: 'It is a special pull.',
        options: const ['Wind', 'Gravity', 'Magic', 'Magnetism'],
        correctAnswer: 'Gravity',
        explanation: 'Gravity is the force that pulls everything towards the center of the Earth.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Sunita Williams', back: 'Astronaut who spent 6 months in space'),
      Flashcard(front: 'Neil Armstrong', back: 'First man to walk on the moon (1969)')
    ],
    revisionNotes: 'On Earth, gravity keeps our feet on the ground. In space, everything floats!',
    commonMistakes: const ['Thinking up and down exist in space'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c12': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand how petroleum is formed',
      'Uses of various oil products (LPG, Kerosene, Petrol)',
      'Ways to save fuel in daily life'
    ],
    examples: const ['Traffic jams wasting fuel', 'Solar energy as an alternative'],
    misconceptions: const ['Oil is formed very quickly under the earth'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which of these is NOT obtained from petroleum?',
        hint: 'Think about what we get from mines vs forests.',
        options: const ['Petrol', 'Diesel', 'Coal', 'Wax'],
        correctAnswer: 'Coal',
        explanation: 'Coal is a solid fossil fuel, while petrol, diesel, and wax are obtained from petroleum.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Adalaj Stepwell location', back: 'Ahmedabad, Gujarat'),
      Flashcard(front: 'Uses of LPG', back: 'Cooking food in homes')
    ],
    revisionNotes: 'Petroleum is called "Black Gold". It takes millions of years to form.',
    commonMistakes: const ['Thinking all fuels are petroleum products'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c13': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Lifestyle in high altitude areas (Leh)',
      'About Changpa tribe and Pashmina wool',
      'Types of houses in different terrains'
    ],
    examples: const ['Rebo tents', 'Lekha for sheep', 'Pashmina shawls'],
    misconceptions: const ['Leh is a hot desert because it is a desert'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the Changpa tribe\'s most precious animal?',
        hint: 'They get wool from it.',
        options: const ['Cow', 'Horse', 'Goat', 'Dog'],
        correctAnswer: 'Goat',
        explanation: 'The special goats provide wool for the famous Pashmina shawls.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Cold Desert of India', back: 'Ladakh'),
      Flashcard(front: 'Pashmina Shawl warmth', back: 'As warm as 6 sweaters')
    ],
    revisionNotes: 'Changpa people live at 5000 meters altitude. Their tents are called Rebo.',
    commonMistakes: const ['Thinking Changpas live in permanent stone houses'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c14': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understanding earthquakes and their impact',
      'Safety measures during an earthquake',
      'Community help during disasters'
    ],
    examples: const ['Kutch earthquake (2001)', 'Building earthquake-resistant houses'],
    misconceptions: const ['Earthquakes can be predicted months in advance'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What should you do first during an earthquake if you are indoors?',
        hint: 'Protect your head.',
        options: const ['Run to the balcony', 'Go under a strong table', 'Use the lift', 'Call friends'],
        correctAnswer: 'Go under a strong table',
        explanation: 'Going under a table protects you from falling objects.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Earthquake help', back: 'Doctors, Army, NGOs, and Neighbors'),
      Flashcard(front: 'Safe place', back: 'Open ground away from buildings')
    ],
    revisionNotes: 'Drop, Cover, and Hold on! Disasters require collective action.',
    commonMistakes: const ['Using elevators during an earthquake'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c15': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'How breathing helps cool or warm things',
      'Function of a stethoscope',
      'Understanding mirrors fogging up'
    ],
    examples: const ['Blowing on hot tea', 'Blowing on cold hands in winter'],
    misconceptions: const ['We only breathe out hot air'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why does a mirror become foggy when we breathe on it?',
        hint: 'Our breath has water vapor.',
        options: const ['Dust in air', 'Water vapor condensing', 'Mirror is dirty', 'CO2 turning into liquid'],
        correctAnswer: 'Water vapor condensing',
        explanation: 'The moist air from our breath touches the cool mirror and turns into tiny water drops.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Stethoscope', back: 'Instrument used to listen to heartbeat'),
      Flashcard(front: 'Breathing rate', back: 'Increases when we run or exercise')
    ],
    revisionNotes: 'Breath can be used to blow a whistle, cool food, or warm hands.',
    commonMistakes: const ['Thinking heartbeat stays the same always'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c16': ConceptNode(
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
    prerequisites: const [],
    dependencies: const ['ss6_c2'],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the importance of cleanliness',
      'Respect all types of work (Dignity of Labour)',
      'Gandhiji\'s views on sanitation'
    ],
    examples: const ['Sabarmati Ashram rules', 'Narayan’s childhood story'],
    misconceptions: const ['Cleaning is the job of only specific communities'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who said "Every person should do every kind of work"?',
        hint: 'He is the Father of our Nation.',
        options: const ['Nehru', 'Gandhiji', 'Ambedkar', 'Patel'],
        correctAnswer: 'Gandhiji',
        explanation: 'Gandhiji believed that no work is low and everyone should clean their own surroundings.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Untouchability', back: 'Unfair practice of treating some people as low'),
      Flashcard(front: 'Bhimrao Ambedkar', back: 'Architect of Indian Constitution who fought against bias')
    ],
    revisionNotes: 'Cleanliness is next to Godliness. Respect everyone who works for us.',
    commonMistakes: const ['Thinking certain jobs are "dirty" and should be avoided'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c17': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Breaking gender barriers in sports',
      'Importance of teamwork over individual scores',
      'Challenges faced by girl athletes'
    ],
    examples: const ['Nagpada Basketball Association', 'Afreen’s story'],
    misconceptions: const ['Certain sports are only for boys'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the most important thing in a team?',
        hint: 'Working together.',
        options: const ['Individual points', 'Team spirit', 'Famous captain', 'New shoes'],
        correctAnswer: 'Team spirit',
        explanation: 'A team wins when players play for the team, not just for themselves.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Gender Bias', back: 'Treating girls and boys differently/unfairly'),
      Flashcard(front: 'NBA', back: 'Nagpada Basketball Association')
    ],
    revisionNotes: 'Sports help in building confidence and breaking social walls.',
    commonMistakes: const ['Focusing only on winning, not playing'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c18': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Reasons for migration (Dams, Jobs, Education)',
      'Problems faced by displaced people in cities',
      'Village life vs City life'
    ],
    examples: const ['Khedi village', 'Jatrya Bhai’s struggle in Mumbai'],
    misconceptions: const ['Cities are always a better place to live than villages'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why was Jatrya Bhai forced to leave his village Khedi?',
        hint: 'A big wall was being built on the river.',
        options: const ['For fun', 'To build a dam', 'Because of a fire', 'To find gold'],
        correctAnswer: 'To build a dam',
        explanation: 'When dams are built, nearby villages are often submerged, forcing people to move.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Migration', back: 'Moving from one place to another for work or safety'),
      Flashcard(front: 'Displacement', back: 'Being forced to leave one\'s home')
    ],
    revisionNotes: 'Villages have fresh air and community; cities have jobs and schools but are crowded.',
    commonMistakes: const ['Thinking all people move to cities by choice'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c19': ConceptNode(
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
    prerequisites: const ['e5_c5'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Evolution of farming techniques',
      'Chemical fertilizers vs Natural manure',
      'Impact of hybrid seeds and monoculture'
    ],
    examples: const ['Undhiya (Gujarati dish)', 'Van-gam village', 'Earthworms as farmer friends'],
    misconceptions: const ['Chemical fertilizers are always better for soil'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which animal is called a "friend of farmers"?',
        hint: 'It lives in the soil.',
        options: const ['Lion', 'Earthworm', 'Dog', 'Cat'],
        correctAnswer: 'Earthworm',
        explanation: 'Earthworms soften the soil and turn waste into manure.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Undhiya', back: 'A traditional winter vegetable dish cooked upside down'),
      Flashcard(front: 'Hybrid Seeds', back: 'Seeds made in labs that need more water and chemicals')
    ],
    revisionNotes: 'Traditional farming used natural seeds and manure. Modern farming uses machines and chemicals.',
    commonMistakes: const ['Thinking tractors are always better than bullocks'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c20': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Importance of forests for Adivasis',
      'Right to Forest Act 2007',
      'Suryamani\'s "Torang" center'
    ],
    examples: const ['Kuduk language', 'Cheraw dance', 'Jhum farming'],
    misconceptions: const ['Adivasis destroy forests'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What does "Torang" mean in Kuduk language?',
        hint: 'It is a place with lots of trees.',
        options: const ['Mountain', 'River', 'Jungle', 'Sky'],
        correctAnswer: 'Jungle',
        explanation: 'Suryamani started Torang to preserve Kuduk culture and forests.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Jhum Farming', back: 'Traditional shifting cultivation in Mizoram'),
      Flashcard(front: 'Right to Forest Act', back: 'People living in forests for 25 years have right over the land')
    ],
    revisionNotes: 'Forests are our collective bank. Cheraw is a famous bamboo dance.',
    commonMistakes: const ['Thinking Jhum farming is done in plains'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c21': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify inherited traits (habits, features)',
      'Understand Gregor Mendel\'s experiments with peas',
      'Adopted vs Biological traits'
    ],
    examples: const ['Curly hair', 'Polio (not inherited)', 'Tallness in pea plants'],
    misconceptions: const ['Diseases like Polio are inherited from parents'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who did experiments with 28,000 pea plants?',
        hint: 'He was a monk.',
        options: const ['Einstein', 'Mendel', 'Darwin', 'Newton'],
        correctAnswer: 'Mendel',
        explanation: 'Gregor Mendel discovered the rules of heredity using pea plants.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Gregor Mendel', back: 'Father of Genetics'),
      Flashcard(front: 'Polio', back: 'Caused by a virus, not inherited from parents')
    ],
    revisionNotes: 'Some traits we get from birth, others we learn from our surroundings.',
    commonMistakes: const ['Confusing learned habits with inherited traits'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'e5_c22': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Life of sugarcane workers',
      'Concept of "Mukadam" (agent)',
      'Impact of seasonal migration on children’s education'
    ],
    examples: const ['Dhanu’s village', 'Working in sugar factories'],
    misconceptions: const ['All farmers have their own land'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is a "Mukadam"?',
        hint: 'He lends money to families.',
        options: const ['A Doctor', 'An Agent/Money lender', 'A Teacher', 'A Driver'],
        correctAnswer: 'An Agent/Money lender',
        explanation: 'Mukadams lend money and tell families where they will work for the next few months.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Caravan', back: 'Group of families moving together with their belongings'),
      Flashcard(front: 'Puranpoli', back: 'Sweet rotis made of gram and jaggery')
    ],
    revisionNotes: 'Seasonal work forces families to move, which often disrupts children\'s studies.',
    commonMistakes: const ['Thinking farmers work all 12 months on the same crop'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 5 ENGLISH (Marigold)
  // ===========================================================================

  'en5_c1': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand rhyming words and adjectives',
      'Learn how to recycle household waste',
      'Describe scenes using sensory words'
    ],
    examples: const ['Scraps turning into "Avial" dish', 'Trundling, mounds, frosty-fizz'],
    misconceptions: const ['Recycling is only for factories (we can do it at home too!)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What dish was made from vegetable scraps in the palace of Travancore?',
        hint: 'It is a famous Kerala dish.',
        options: const ['Sambar', 'Avial', 'Dosa', 'Idli'],
        correctAnswer: 'Avial',
        explanation: 'Avial was made by the cook using vegetable bits that were going to be thrown away.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Wonderful Waste', back: 'Idea that waste can be useful if we are creative'),
      Flashcard(front: 'Rhyming with "Sight"', back: 'Bright, Light, Night')
    ],
    revisionNotes: 'Ice-cream man poem focus on imagery. Wonderful Waste story focus on resourcefulness.',
    commonMistakes: const ['Spelling of "Wonderful"', 'Confusing adjectives with verbs'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c2': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Importance of working together to achieve goals',
      'Wisdom of elders (Panchatantra-style story)',
      'Learning to follow advice'
    ],
    examples: const ['Geese escaping the hunter', 'Passing the ball in basketball'],
    misconceptions: const ['One person can do everything alone'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why did the wise old bird tell the other geese to destroy the creeper?',
        hint: 'Creepers grow and become strong.',
        options: const ['It was ugly', 'A hunter could climb it', 'It was blocking sun', 'For no reason'],
        correctAnswer: 'A hunter could climb it',
        explanation: 'The wise bird knew that a strong creeper would help a hunter climb the tree.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Teamwork', back: 'Working together to make our dream work'),
      Flashcard(front: 'Unity', back: 'Together we are strong')
    ],
    revisionNotes: 'Listen to advice from those who have more experience.',
    commonMistakes: const ['Ignoring the "moral of the story"'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Poetic devices in "My Shadow"',
      'Adventure and survival skills',
      'Using imagination in writing'
    ],
    examples: const ['Footprint on the sand', 'Shadow growing taller and shorter'],
    misconceptions: const ['Robinson Crusoe was never afraid'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What did Robinson Crusoe see on the sand that frightened him?',
        hint: 'It belongs to a foot.',
        options: const ['A snake', 'A footprint', 'A shell', 'A boat'],
        correctAnswer: 'A footprint',
        explanation: 'He was lonely for years, so a human footprint made him think of savages.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Buttercup', back: 'A yellow flower mentioned in the poem'),
      Flashcard(front: 'Crusoe\'s companion', back: 'He later found a man and named him Friday')
    ],
    revisionNotes: 'Shadows change size based on light position. Crusoe lived on a desert island.',
    commonMistakes: const ['Confusing "scared" with "scary"'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c4': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Expression of emotions through poetry',
      'Dynamics of siblings and academic expectations',
      'Difference between bookish knowledge and life experience'
    ],
    examples: const ['Bhaiya vs Munna', 'Crying until the pillow is soaked'],
    misconceptions: const ['Studying all the time is the only way to be wise'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who was three years older but five years ahead in school?',
        hint: 'He studied very hard.',
        options: const ['Munna', 'Bhaiya', 'The Father', 'The Teacher'],
        correctAnswer: 'Bhaiya',
        explanation: 'Bhaiya took his studies very seriously but struggled to pass.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Crying', back: 'A way to let out emotions to feel happy later'),
      Flashcard(front: 'Foundation', back: 'Strong base (Bhaiya wanted a strong base in English)')
    ],
    revisionNotes: 'Experience is as important as books. Respect your elders\' wisdom.',
    commonMistakes: const ['Thinking Bhaiya was mean (he was actually caring)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c5': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify traits of laziness',
      'Narrative structure of a legend',
      'Using past tense in storytelling'
    ],
    examples: const ['Rip sleeping for 20 years', 'Fred the frog ignoring his mother'],
    misconceptions: const ['Rip Van Winkle is a true historical story (it is a legend)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where did Rip Van Winkle live?',
        hint: 'Near a mountain range.',
        options: const ['Himalayas', 'Kaatskill Mountains', 'Alps', 'Andes'],
        correctAnswer: 'Kaatskill Mountains',
        explanation: 'Rip lived in a village at the foot of the Kaatskill mountains.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Fred', back: 'The name of the lazy frog'),
      Flashcard(front: 'Companion', back: 'Rip\'s dog named Wolf')
    ],
    revisionNotes: 'Legends often involve magic or mysterious events. Laziness leads to missed life.',
    commonMistakes: const ['Spelling of "Van Winkle"'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand how to participate in a discussion',
      'Identify traits of talkative vs quiet people',
      'Arabic folklore themes'
    ],
    examples: const ['Jane being quiet in class', 'The Barber wasting Sultan\'s time'],
    misconceptions: const ['Talking a lot means you are very wise'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why did the Sultan give all his food to the Barber?',
        hint: 'He wanted to get his head shaved quickly.',
        options: const ['He was generous', 'To get rid of him', 'The food was bad', 'He was not hungry'],
        correctAnswer: 'To get rid of him',
        explanation: 'The Sultan was desperate for the Barber to stop talking and finish the work.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Discussion', back: 'Talking together in a group about a topic'),
      Flashcard(front: 'Defect', back: 'A fault or problem (The Barber called his brothers defective)')
    ],
    revisionNotes: 'Active listening is part of a good discussion. Arabian Nights is a collection of famous stories.',
    commonMistakes: const ['Interrupting others during discussion'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c7': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Compare real world with imaginary Topsy-turvy land',
      'Understand the concept of relative size (Giants)',
      'Descriptive writing skills'
    ],
    examples: const ['Walking on hands in Topsy-turvy land', 'Gulliver in Brobdingnag (Land of Giants)'],
    misconceptions: const ['Gulliver only went to the land of small people (Lilliput)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'In Topsy-turvy land, where do the boats travel?',
        hint: 'It is the opposite of water.',
        options: const ['In the sky', 'On the streets', 'In the sea', 'Underground'],
        correctAnswer: 'On the streets',
        explanation: 'In this imaginary land, boats travel on streets and you walk on your hands.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Brobdingnag', back: 'The land of Giants Gulliver visited'),
      Flashcard(front: 'Pleasure', back: 'A feeling of happy satisfaction')
    ],
    revisionNotes: 'Use adjectives like "enormous", "monstrous", "tiny" to describe scale.',
    commonMistakes: const ['Confusing the sequence of Gulliver\'s voyages'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify behaviors that win or lose friends',
      'Impact of bullying on others',
      'Learning to share and be kind'
    ],
    examples: const ['Hari pinching others', 'The girl who wouldn\'t share her sweets'],
    misconceptions: const ['Bullying makes you look "cool" or strong'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What lesson did Hari learn at the seaside?',
        hint: 'The crabs pinched him.',
        options: const ['How to swim', 'How it feels to be pinched', 'How to catch crabs', 'To eat more cake'],
        correctAnswer: 'How it feels to be pinched',
        explanation: 'After the crabs pinched him, Hari realized how much he hurt his classmates.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Sharing', back: 'A key to making friends'),
      Flashcard(front: 'Empathy', back: 'Understanding how someone else feels')
    ],
    revisionNotes: 'Be nice to others if you want them to be nice to you. Sharing is caring.',
    commonMistakes: const ['Thinking being a bystander is okay'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c9': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Contrast city life with quiet life',
      'Understand different modes of transport',
      'Adventure across continents (Phileas Fogg)'
    ],
    examples: const ['Subways and elevators in cities', 'The train through the Rocky Mountains'],
    misconceptions: const ['"Around the World in 80 Days" is a modern story (it was written in 1872)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who was the main character in "Around the World"?',
        hint: 'He made a bet to travel the world.',
        options: const ['Robinson Crusoe', 'Phileas Fogg', 'Gulliver', 'Rip Van Winkle'],
        correctAnswer: 'Phileas Fogg',
        explanation: 'Phileas Fogg took the challenge to travel the world in exactly 80 days.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Subway', back: 'An underground electric railroad'),
      Flashcard(front: 'Rocky Mountains', back: 'Mountain range in North America')
    ],
    revisionNotes: 'The world is a large place with diverse people and landscapes.',
    commonMistakes: const ['Spelling of "Phileas"'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en5_c10': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Qualities of a good leader (Justice, Empathy)',
      'Coming of age and learning skills (Malu the Polar Bear)',
      'Manipur folklore and culture'
    ],
    examples: const ['Malu learning to swim', 'Sanatombi becoming the Meithel Leima'],
    misconceptions: const ['A leader is only the strongest person'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why did the Ningthou choose Sanatombi as the future ruler?',
        hint: 'She felt the pain of nature.',
        options: const ['She was eldest', 'She won a race', 'She was kind and empathetic', 'She was strong'],
        correctAnswer: 'She was kind and empathetic',
        explanation: 'The king chose her because she could feel the pain of people, animals, and trees.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Ningthou', back: 'The King (in Manipur)'),
      Flashcard(front: 'Malu Bhalu', back: 'A brave polar bear girl')
    ],
    revisionNotes: 'True leadership involves thinking about everyone\'s well-being.',
    commonMistakes: const ['Confusing the three sons with the daughter\'s success'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 5 HINDI (Rimjhim)
  // ===========================================================================

  'h5_c1': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand Tibetan folklore',
      'Identify traits of wit and intelligence',
      'Learn Hindi vocabulary related to stories'
    ],
    examples: const ['Lonpo Gar\'s son', 'The girl who made a rope of ash'],
    misconceptions: const ['Thinking stories from other countries are not part of NCERT'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Lonpo Gar was a minister of which place?',
        hint: 'It is a place with high mountains.',
        options: const ['India', 'Tibet', 'Nepal', 'China'],
        correctAnswer: 'Tibet',
        explanation: 'Lonpo Gar was the minister of Sonam Gampo, the King of Tibet.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Haazirjawabi', back: 'Wittiness / Quick in replying'),
      Flashcard(front: 'Bholapan', back: 'Innocence (trait of the son)')
    ],
    revisionNotes: 'Wit can solve problems that strength cannot.',
    commonMistakes: const ['Spelling of Tibetan names in Hindi'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c2': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about different harvest festivals across India',
      'Understand the cultural significance of crops',
      'Hindi names for regional festivals'
    ],
    examples: const ['Makar Sankranti', 'Bihu', 'Pongal', 'Lohri'],
    misconceptions: const ['All Indians celebrate the same festival in the same way'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which festival is celebrated in Assam to mark harvest?',
        hint: 'It involves dancing and music.',
        options: const ['Pongal', 'Lohri', 'Bihu', 'Onam'],
        correctAnswer: 'Bihu',
        explanation: 'Bihu is the major harvest festival of Assam.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Khichdi', back: 'A festival name for Makar Sankranti in Bihar/UP'),
      Flashcard(front: 'Sohrai', back: 'Harvest festival of Adivasis in Jharkhand')
    ],
    revisionNotes: 'Festivals bring people together and celebrate nature\'s gifts.',
    commonMistakes: const ['Confusing states with their specific festivals'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Enjoy the rhythm of Hindi poetry',
      'Learn names of toys and mythological characters',
      'Express desire through verse'
    ],
    examples: const ['Ramayana references (Ram, Kaushalya)', 'Toy motor-cars and whistles'],
    misconceptions: const ['The poem is only about buying toys'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who wrote the poem "Khilaunewala"?',
        hint: 'She is a famous Hindi poetess.',
        options: const ['Mahadevi Verma', 'Subhadra Kumari Chauhan', 'Nirmala Deshpande', 'Sarojini Naidu'],
        correctAnswer: 'Subhadra Kumari Chauhan',
        explanation: 'The poem was composed by Subhadra Kumari Chauhan.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Talwar', back: 'Sword'),
      Flashcard(front: 'Teer-kaman', back: 'Bow and arrow')
    ],
    revisionNotes: 'The child wants to be like Ram and kill demons like Tadka.',
    commonMistakes: const ['Identifying the poet correctly'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c4': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about stone carving (sculpture)',
      'Life at the time of Emperor Akbar',
      'Passion for craft at a young age'
    ],
    examples: const ['Keshav (the young artist)', 'Fatehpur Sikri construction'],
    misconceptions: const ['Kings were always scary and unapproachable'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What was the age of Keshav?',
        hint: 'He was a young boy.',
        options: const ['10 years', '12 years', '15 years', '8 years'],
        correctAnswer: '10 years',
        explanation: 'Keshav was a 10-year-old boy who was learning stone carving.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Fankar', back: 'Artist / Craftsman'),
      Flashcard(front: 'Chaini-Hathauda', back: 'Chisel and Hammer')
    ],
    revisionNotes: 'Hard work and talent are respected even by Kings.',
    commonMistakes: const ['Spelling of "Fatehpur Sikri"'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c5': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Inspirational story of Ila Sachani',
      'Overcoming physical disability',
      'Traditional embroidery styles'
    ],
    examples: const ['Kasuti embroidery', 'Kashmiri work', 'Using feet for sewing'],
    misconceptions: const ['Disabled people cannot do intricate handwork'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Ila Sachani was an expert in which craft?',
        hint: 'It involves needle and thread.',
        options: const ['Pottery', 'Embroidery', 'Painting', 'Cooking'],
        correctAnswer: 'Embroidery',
        explanation: 'Despite having disabled hands, she learned to embroider with her feet.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Zardozi', back: 'A type of heavy and elaborate metal embroidery'),
      Flashcard(front: 'Ila\'s state', back: 'Gujarat')
    ],
    revisionNotes: 'Willpower can turn impossible into possible.',
    commonMistakes: const ['Thinking she used her hands for embroidery'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Evolution of letters and messages',
      'Function of PIN codes',
      'Use of pigeons in ancient times'
    ],
    examples: const ['Harkara (messengers)', 'Speed post', 'Email vs Letter'],
    misconceptions: const ['PIN code is just a random number'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the full form of PIN in PIN Code?',
        hint: 'It relates to the post office.',
        options: const ['Personal Id Number', 'Postal Index Number', 'Public Info Net', 'Private Int Node'],
        correctAnswer: 'Postal Index Number',
        explanation: 'PIN stands for Postal Index Number, used to sort mail easily.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Pigeon post', back: 'Using Homa pigeons to carry messages'),
      Flashcard(front: 'PIN digits', back: '6 digits in India')
    ],
    revisionNotes: 'Addresses must be complete with name, house number, area, and PIN.',
    commonMistakes: const ['Writing wrong PIN codes'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c7': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the format of an interview',
      'Life challenges of a postman in hilly areas',
      'Value of a postman in remote villages'
    ],
    examples: const ['Kunwar Singh (the postman)', 'Shimla district challenges'],
    misconceptions: const ['Postmen only deliver letters in cities'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who was interviewed in this chapter?',
        hint: 'He is a postman.',
        options: const ['Keshav', 'Lonpo Gar', 'Kunwar Singh', 'Bishan'],
        correctAnswer: 'Kunwar Singh',
        explanation: 'Kunwar Singh from Shimla district shares his experience as a postman.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Interview', back: 'A conversation where questions are asked and answered'),
      Flashcard(front: 'Packer', back: 'A post office staff member who packs mail')
    ],
    revisionNotes: 'Postmen are trusted messengers in villages, carrying pensions and money orders.',
    commonMistakes: const ['Missing the interview context'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Contrast traditional books with screen-based reading',
      'Imagining a school with mechanical teachers',
      'Value of social interaction in schools'
    ],
    examples: const ['Tommy and Kummi', 'Finding a real paper book'],
    misconceptions: const ['Mechanical teachers are better than human teachers'],
    practiceExercises: const [
      PracticeExercise(
        question: 'In the future story, where did students study?',
        hint: 'It was inside their own house.',
        options: const ['A big building', 'A park', 'A room in their house', 'A library'],
        correctAnswer: 'A room in their house',
        explanation: 'The story imagines students having a mechanical teacher in a room at home.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Mechanical Teacher', back: 'A robot or computer that teaches'),
      Flashcard(front: 'Real Book', back: 'A book made of paper with printed words')
    ],
    revisionNotes: 'Traditional schools allow children to play and learn together.',
    commonMistakes: const ['Confusing the past with the future setting of the story'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c9': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the feelings of a non-verbal child',
      'Learn to empathize with people who are different',
      'Express helplessness through poetry'
    ],
    examples: const ['Ratan (the child)', 'Mother\'s constant gaze'],
    misconceptions: const ['People who cannot speak do not have thoughts or feelings'],
    practiceExercises: const [
      PracticeExercise(
        question: 'How did Ratan communicate with other children?',
        hint: 'He used his eyes and hands.',
        options: const ['By writing', 'By signs/gestures', 'By singing', 'By shouting'],
        correctAnswer: 'By signs/gestures',
        explanation: 'Ratan was unable to speak, so he used gestures and expressions to communicate.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Bebasi', back: 'Helplessness'),
      Flashcard(front: 'Poet', back: 'Kunwar Narain')
    ],
    revisionNotes: 'Everyone deserves friends, even if they communicate differently.',
    commonMistakes: const ['Ignoring the emotional depth of the poem'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c10': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand children\'s desire for freedom',
      'Learn about role-reversal in a family',
      'Hindi synonyms for power and rules'
    ],
    examples: const ['Arif and Salim', 'Giving orders to elders'],
    misconceptions: const ['The story is about becoming a real king'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What did Arif and Salim want from their father (Abba)?',
        hint: 'They wanted to be in charge for a day.',
        options: const ['New clothes', 'One day of power', 'Money', 'Vacation'],
        correctAnswer: 'One day of power',
        explanation: 'They wanted to treat the elders the way elders treated them for one day.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Badshahat', back: 'Kingship / Sovereignty'),
      Flashcard(front: 'Pabandi', back: 'Restriction / Ban')
    ],
    revisionNotes: 'Empathy grows when we experience life from another person\'s perspective.',
    commonMistakes: const ['Missing the humour in the boys\' actions'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c11': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about Burmese culture and setting',
      'Follow the consequences of lying/making excuses',
      'Dialogue delivery in a play'
    ],
    examples: const ['Koko hiding his rice cakes', 'Friends visiting unexpectedly'],
    misconceptions: const ['Koko was a mean person (he was just hungry and protective)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why did Koko hide the rice cakes?',
        hint: 'He didn\'t want to share.',
        options: const ['They were poisoned', 'They were stale', 'He wanted to eat them all', 'They were for his sister'],
        correctAnswer: 'He wanted to eat them all',
        explanation: 'Koko loved rice cakes and didn\'t want to share them with his friends.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Chawal ki Rotiyan', back: 'Rice cakes / Breads'),
      Flashcard(front: 'Bahana', back: 'Excuse')
    ],
    revisionNotes: 'Sharing with friends makes the food taste better and keeps the heart light.',
    commonMistakes: const ['Thinking the play is set in India'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c12': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Humorous take on a foolish kingdom (Andher Nagari)',
      'Rhyme scheme and flow of the poem',
      'Moral lesson on logic and justice'
    ],
    examples: const ['Everything costing one "Taka"', 'The wall falling and looking for a culprit'],
    misconceptions: const ['The Guru was selfish for leaving the Chela'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What was the name of the kingdom in the poem?',
        hint: 'It was a dark/foolish place.',
        options: const ['Sunder Nagari', 'Andher Nagari', 'Ujala Nagari', 'Lal Nagari'],
        correctAnswer: 'Andher Nagari',
        explanation: 'Andher Nagari was a kingdom where the king was foolish and rules were non-existent.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Andher Nagari', back: 'Kingdom of Chaos'),
      Flashcard(front: 'Taka', back: 'A small unit of currency')
    ],
    revisionNotes: 'A wise person stays away from places where there is no logic or justice.',
    commonMistakes: const ['Confusing the Chela\'s greed with wisdom'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c13': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Relationship between grandchild and grandparent',
      'R.K. Narayan\'s storytelling style (Malgudi context)',
      'Handling pride and boasting'
    ],
    examples: const ['Swami telling Dadi about Rajam', 'Dadi\'s old stories of Grandfather'],
    misconceptions: const ['Dadi was ignoring Swami (she was just old and sleepy)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who was the hero of Swami\'s stories?',
        hint: 'He was a brave boy with a gun.',
        options: const ['Mani', 'Rajam', 'Sankar', 'The Postman'],
        correctAnswer: 'Rajam',
        explanation: 'Swami was very proud of his friend Rajam and told many stories about him to Dadi.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Swami\'s real name', back: 'Swaminathan'),
      Flashcard(front: 'Boasting', back: 'Shekhi baghaarna')
    ],
    revisionNotes: 'Listening to elders\' stories connects us to our family history.',
    commonMistakes: const ['Thinking the story is set in a modern city'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c14': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the perspective of a child about danger',
      'Learn about the habitat of tigers',
      'Conversational style in Hindi poetry'
    ],
    examples: const ['Tiger living in a cave', 'Child warning Baba not to go out at night'],
    misconceptions: const ['Tigers only come to villages to hurt people'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is warning the elders about the tiger?',
        hint: 'He is a young child.',
        options: const ['The King', 'The Postman', 'The 5-year-old child', 'The Hunter'],
        correctAnswer: 'The 5-year-old child',
        explanation: 'The poem is a conversation where a child is telling his father about a tiger sighting.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Baba', back: 'Father / Grandfather'),
      Flashcard(front: 'Sachet', back: 'Alert / Careful')
    ],
    revisionNotes: 'Wildlife often overlaps with human habitats in some areas. Caution is key.',
    commonMistakes: const ['Thinking the tiger actually entered the house'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c15': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Moral value of protecting animals',
      'Challenges of living in hilly areas',
      'Heroism shown by a young boy'
    ],
    examples: const ['Bishan saving a wounded Pheasant (Teetar)', 'Hiding from the hunters'],
    misconceptions: const ['Hunting is always a "sport" (it is often cruel/illegal)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which bird did Bishan save?',
        hint: 'It is a small game bird.',
        options: const ['Peacock', 'Pheasant (Teetar)', 'Pigeon', 'Parrot'],
        correctAnswer: 'Pheasant (Teetar)',
        explanation: 'Bishan risked his safety to save a pheasant that was wounded by hunters.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Dileri', back: 'Bravery / Courage'),
      Flashcard(front: 'Khet', back: 'Fields (Step fields in hills)')
    ],
    revisionNotes: 'Compassion for living beings is the highest form of bravery.',
    commonMistakes: const ['Spelling of "Teetar" in Hindi'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c16': ConceptNode(
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
    prerequisites: const ['e5_c6'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the source of water in our taps',
      'Learn about water shortage and its causes',
      'Importance of preserving ponds and lakes'
    ],
    examples: const ['Groundwater levels', 'Encroachment on old ponds'],
    misconceptions: const ['Water comes only from the tap (it comes from rivers/ground)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why are our groundwater levels going down?',
        hint: 'We are covering the soil and losing ponds.',
        options: const ['Less rain', 'More people', 'Loss of ponds and concrete roads', 'Magic'],
        correctAnswer: 'Loss of ponds and concrete roads',
        explanation: 'When we fill up ponds and cover soil with concrete, rain water cannot go into the ground.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Jal Chakra', back: 'Water Cycle'),
      Flashcard(front: 'Bhu-jal', back: 'Groundwater')
    ],
    revisionNotes: 'Save every drop. Revive traditional water bodies.',
    commonMistakes: const ['Thinking rain is the only solution for water crisis'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c17': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Appreciate the beauty of a river in different seasons',
      'Identify onomatopoeic words (words that sound like what they mean)',
      'Tagore\'s poetic style'
    ],
    examples: const ['Kans flowers', 'Chik-chik of Mainas', 'Kich-pich sounds'],
    misconceptions: const ['Rivers are the same all year round (they change in summer/monsoon)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who wrote the poem "Chhoti si Hamari Nadi"?',
        hint: 'He is India\'s first Nobel Laureate.',
        options: const ['Premchand', 'Rabindranath Tagore', 'Nirala', 'Pant'],
        correctAnswer: 'Rabindranath Tagore',
        explanation: 'The poem was originally written by Rabindranath Tagore.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Dhaar', back: 'Flow / Current'),
      Flashcard(front: 'Ghamasaan', back: 'Very intense / Heavy (rain)')
    ],
    revisionNotes: 'Summer: River is shallow. Monsoon: River is full and fast.',
    commonMistakes: const ['Misidentifying the poet'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h5_c18': ConceptNode(
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
    prerequisites: const ['e5_c9'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Story of Jawaharlal Nehru\'s trek to Amarnath',
      'Challenges of breathing and trekking in high altitude',
      'Awe and respect for the Himalayas'
    ],
    examples: const ['Zojila pass', 'Mataun pass', 'Crevasses hidden in snow'],
    misconceptions: const ['Nehru only did politics (he was also an adventurer)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where was Nehru trying to reach in this story?',
        hint: 'A holy cave in the Himalayas.',
        options: const ['Kedarnath', 'Amarnath', 'Badrinath', 'Gangotri'],
        correctAnswer: 'Amarnath',
        explanation: 'Nehru was on a trek from Zojila to reach the Amarnath cave.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Chunauti', back: 'Challenge'),
      Flashcard(front: 'Him-shikhar', back: 'Snow peaks')
    ],
    revisionNotes: 'Himalayas are beautiful but require great caution and preparation to climb.',
    commonMistakes: const ['Thinking he reached the destination (he had to return due to bad weather/cracks)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 6 MATHEMATICS
  // ===========================================================================

  'm6_c1': ConceptNode(
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
    prerequisites: const ['m5_c1'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Compare large numbers effectively',
      'Use Indian and International place value systems',
      'Understand Estimation and Roman Numerals'
    ],
    examples: const ['1 million = 10 lakhs', 'Estimation of 4875 to nearest thousand is 5000'],
    misconceptions: const ['Thinking Roman numerals have a symbol for zero (they do not)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Insert commas in International system: 987654321',
        hint: 'Use groups of 3.',
        options: const ['98,76,54,321', '987,654,321', '9,8,7,6,5,4,3,2,1', '9876,54321'],
        correctAnswer: '987,654,321',
        explanation: 'International system uses 3-digit groupings: Millions, Thousands, Ones.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Roman Numeral L', back: '50'),
      Flashcard(front: 'Roman Numeral C', back: '100'),
      Flashcard(front: 'Roman Numeral D', back: '500'),
      Flashcard(front: 'Roman Numeral M', back: '1000')
    ],
    revisionNotes: 'Estimation makes big calculations easier and faster. Roman numerals follow addition/subtraction rules.',
    commonMistakes: const ['Writing IVVV for 15 (cannot repeat V)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c2': ConceptNode(
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
    prerequisites: const ['m5_c1'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Difference between Natural and Whole numbers',
      'Representation on number line',
      'Commutative, Associative, and Distributive properties'
    ],
    examples: const ['a + b = b + a (Commutative)', '0 is the additive identity'],
    misconceptions: const ['Division by zero is zero (it is undefined)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the successor of 0?',
        hint: 'Add 1 to the number.',
        options: const ['-1', '0', '1', 'None'],
        correctAnswer: '1',
        explanation: '0 + 1 = 1.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Natural Numbers', back: 'Counting numbers 1, 2, 3...'),
      Flashcard(front: 'Whole Numbers', back: 'Natural numbers including 0')
    ],
    revisionNotes: 'Property of Distributivity: a * (b + c) = (a * b) + (a * c).',
    commonMistakes: const ['Applying commutative property to subtraction'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c3': ConceptNode(
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
    prerequisites: const ['m5_c6'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Apply divisibility tests (2 to 11)',
      'Find prime and composite numbers (Eratosthenes Sieve)',
      'Calculate HCF and LCM of multiple numbers'
    ],
    examples: const ['Number is divisible by 3 if sum of digits is divisible by 3', '2 is the only even prime'],
    misconceptions: const ['1 is a prime number (it is neither prime nor composite)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the HCF of 15 and 20?',
        hint: 'Find the largest number that divides both.',
        options: const ['60', '1', '5', '10'],
        correctAnswer: '5',
        explanation: 'Factors of 15: 1, 3, 5, 15. Factors of 20: 1, 2, 4, 5, 10, 20. Largest common is 5.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Perfect Number', back: 'Sum of its factors equals twice the number (e.g., 6)'),
      Flashcard(front: 'Co-prime', back: 'Two numbers having only 1 as common factor')
    ],
    revisionNotes: 'If a number is divisible by 9, it is also divisible by 3.',
    commonMistakes: const ['Confusing LCM calculation with HCF'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c4': ConceptNode(
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
    prerequisites: const ['m5_c2'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Define point, line, ray, and line segment',
      'Distinguish between open and closed curves',
      'Parts of a polygon and circle'
    ],
    examples: const ['Diameter is twice the radius', 'A triangle is a 3-sided polygon'],
    misconceptions: const ['A ray is same as a line (ray has one end point, line has zero)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which of these has infinite length and no end points?',
        hint: 'It goes on forever in both directions.',
        options: const ['Ray', 'Line Segment', 'Line', 'Point'],
        correctAnswer: 'Line',
        explanation: 'A line has no ends and extends infinitely.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Chord', back: 'Line segment joining two points on a circle'),
      Flashcard(front: 'Sector', back: 'Region bounded by an arc and two radii')
    ],
    revisionNotes: 'Geometry comes from "Geo" (Earth) and "Metron" (Measurement).',
    commonMistakes: const ['Confusing Sector with Segment in a circle'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c5': ConceptNode(
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
    prerequisites: const ['m5_c2', 'm5_c9'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Measure angles using a protractor',
      'Classify triangles by sides and angles',
      'Identify types of quadrilaterals (Parallelogram, Rhombus, etc.)'
    ],
    examples: const ['Equilateral triangle has 3 equal sides', 'Protractor for measuring degrees'],
    misconceptions: const ['Thinking every rectangle is a square (every square is a rectangle)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What do you call a triangle with two equal sides?',
        hint: 'It starts with I.',
        options: const ['Scalene', 'Equilateral', 'Isosceles', 'Right-angled'],
        correctAnswer: 'Isosceles',
        explanation: 'Isosceles triangles have two sides of the same length.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Reflex Angle', back: 'Greater than 180 and less than 360'),
      Flashcard(front: 'Prism', back: '3D shape with same base and top')
    ],
    revisionNotes: 'Clock directions: 1/4 turn = 90 deg, 1/2 turn = 180 deg.',
    commonMistakes: const ['Misreading the scale of a protractor'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c6': ConceptNode(
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
    prerequisites: const ['m6_c2'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the need for negative numbers',
      'Compare integers on a number line',
      'Perform addition and subtraction of integers'
    ],
    examples: const ['Temperature below zero', 'Spending money as a negative value'],
    misconceptions: const ['Thinking -10 is bigger than -2 (actually -2 is closer to zero, so it\'s bigger)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is -5 + 8?',
        hint: 'Start at -5 on number line and move 8 steps right.',
        options: const ['13', '-13', '3', '-3'],
        correctAnswer: '3',
        explanation: '-5 + 8 = 3.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Integer', back: 'Whole numbers and their negatives'),
      Flashcard(front: 'Zero', back: 'Neither positive nor negative')
    ],
    revisionNotes: 'Subtracting a negative number is like adding its positive counterpart.',
    commonMistakes: const ['Signs errors during addition/subtraction'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c7': ConceptNode(
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
    prerequisites: const ['m5_c4'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Proper, Improper, and Mixed fractions',
      'Simplifying fractions to lowest terms',
      'Adding and subtracting like and unlike fractions'
    ],
    examples: const ['3/2 is an improper fraction (1 1/2 as mixed)', '1/2 + 1/4 = 3/4'],
    misconceptions: const ['You can add numerators even if denominators are different'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Reduce to simplest form: 12/18',
        hint: 'Divide both by their HCF (6).',
        options: const ['2/3', '3/2', '6/9', '4/6'],
        correctAnswer: '2/3',
        explanation: '12/6 = 2, 18/6 = 3. So 2/3.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Proper Fraction', back: 'Numerator < Denominator'),
      Flashcard(front: 'Like Fractions', back: 'Fractions with same denominator')
    ],
    revisionNotes: 'Find LCM of denominators to add unlike fractions.',
    commonMistakes: const ['Forgetting to find common denominator'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c8': ConceptNode(
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
    prerequisites: const ['m5_c10'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Represent decimals on number line',
      'Compare decimals like 0.07 and 0.1',
      'Add and subtract decimal numbers'
    ],
    examples: const ['0.5 = 5/10', '0.07 < 0.1 because 0.07 < 0.10'],
    misconceptions: const ['Adding 1.2 and 0.03 as 0.15 (should be 1.23)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Write 4 tens and 2 tenths as a decimal.',
        hint: '40 + 2/10.',
        options: const ['4.2', '42.0', '40.2', '0.42'],
        correctAnswer: '40.2',
        explanation: '4 tens = 40. 2 tenths = 0.2. Total = 40.2.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Decimals in Money', back: '100 paise = 1 rupee'),
      Flashcard(front: 'Decimals in Weight', back: '1000g = 1kg')
    ],
    revisionNotes: 'Align decimal points vertically when adding or subtracting.',
    commonMistakes: const ['Misaligning digits during addition'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c9': ConceptNode(
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
    prerequisites: const ['m5_c12'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Record data using tally marks',
      'Construct and interpret Pictographs',
      'Draw Bar Graphs for discrete data'
    ],
    examples: const ['One symbol = 10 students in a pictograph', 'Scale of 1 unit = 100 people in bar graph'],
    misconceptions: const ['Pictographs are just for fun and not accurate'],
    practiceExercises: const [
      PracticeExercise(
        question: 'If a star symbol in a pictograph represents 5 children, how many stars represent 20 children?',
        hint: 'Divide 20 by 5.',
        options: const ['2', '3', '4', '5'],
        correctAnswer: '4',
        explanation: '20 / 5 = 4 symbols.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Pictograph', back: 'Representing data through pictures of objects'),
      Flashcard(front: 'Bar Graph', back: 'Representing data using bars of uniform width')
    ],
    revisionNotes: 'Scale selection is critical for a clear graph.',
    commonMistakes: const ['Uneven width of bars in a bar graph'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c10': ConceptNode(
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
    prerequisites: const ['m5_c11'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Find perimeter of regular polygons using formulas',
      'Calculate area of rectangle and square',
      'Solve daily life problems involving fencing and tiling'
    ],
    examples: const ['Perimeter of hexagon = 6 * side', 'Area of square = side * side'],
    misconceptions: const ['Thinking area and perimeter are the same thing'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Find perimeter of equilateral triangle with side 5cm.',
        hint: '3 * side.',
        options: const ['10 cm', '15 cm', '25 cm', '5 cm'],
        correctAnswer: '15 cm',
        explanation: '3 * 5 = 15cm.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Perimeter of Rectangle', back: '2 * (Length + Breadth)'),
      Flashcard(front: 'Area of Rectangle', back: 'Length * Breadth')
    ],
    revisionNotes: 'Perimeter is length of boundary. Area is surface covered.',
    commonMistakes: const ['Calculation errors in addition/multiplication'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c11': ConceptNode(
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
    prerequisites: const ['m5_c7'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand variables as letters replacing numbers',
      'Translate simple statements into algebraic expressions',
      'Introduction to equations and solutions'
    ],
    examples: const ['Matchstick patterns: 2n for number of matchsticks', 'x + 5 = 12'],
    misconceptions: const ['Thinking a variable has a fixed value always (it varies!)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'If "x" represents age now, what is age 5 years ago?',
        hint: 'Go back in time.',
        options: const ['x + 5', '5x', 'x - 5', 'x / 5'],
        correctAnswer: 'x - 5',
        explanation: '5 years ago means subtraction: x - 5.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Variable', back: 'A letter that can take various numerical values'),
      Flashcard(front: 'Equation', back: 'Condition on a variable with an equality sign')
    ],
    revisionNotes: 'Algebra helps us solve problems by generalizing rules.',
    commonMistakes: const ['Confusing 2x with x + 2'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'm6_c12': ConceptNode(
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
    prerequisites: const ['m6_c7'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Compare quantities using ratios',
      'Check if two ratios are in proportion',
      'Apply Unitary Method to solve problems'
    ],
    examples: const ['Ratio of boys to girls 3:4', 'If 6 cans cost 210, cost of 4 cans is?'],
    misconceptions: const ['Comparing values with different units directly (must convert first)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Are 15, 45, 40, 120 in proportion?',
        hint: 'Check if 15/45 = 40/120.',
        options: const ['Yes', 'No'],
        correctAnswer: 'Yes',
        explanation: '15/45 = 1/3 and 40/120 = 1/3. They are equal.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Ratio', back: 'Comparison of two quantities by division'),
      Flashcard(front: 'Unitary Method', back: 'Finding value of one unit then many')
    ],
    revisionNotes: 'Ratios have no units.',
    commonMistakes: const ['Changing the order of terms in a ratio'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 6 SCIENCE
  // ===========================================================================

  's6_c1': ConceptNode(
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
    prerequisites: const ['e5_c3'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Identify nutrients: Carbohydrates, Proteins, Fats, Vitamins, Minerals',
      'Test for starch, protein, and fats',
      'Understand Balanced Diet and Deficiency diseases'
    ],
    examples: const ['Iodine test for starch', 'Vitamin C prevents Scurvy'],
    misconceptions: const ['Fats are always bad (essential for energy)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which nutrient is known as "body building" food?',
        hint: 'It helps in growth.',
        options: const ['Carbohydrates', 'Proteins', 'Vitamins', 'Fats'],
        correctAnswer: 'Proteins',
        explanation: 'Proteins are needed for the growth and repair of our body.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Roughage', back: 'Dietary fibres that help in digestion'),
      Flashcard(front: 'Scurvy', back: 'Deficiency of Vitamin C')
    ],
    revisionNotes: 'Carbohydrates and fats provide energy. Proteins are for growth.',
    commonMistakes: const ['Thinking water is a nutrient (it is essential but not a nutrient)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c2': ConceptNode(
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
    prerequisites: const ['e5_c7'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Classify objects based on lustre, hardness, and transparency',
      'Understand solubility and density (floating/sinking)',
      'Purpose of grouping materials'
    ],
    examples: const ['Glass is transparent', 'Wood is opaque', 'Salt is soluble'],
    misconceptions: const ['All metals are hard (Sodium is soft)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'A material through which you can see clearly is?',
        hint: 'Like window glass.',
        options: const ['Opaque', 'Translucent', 'Transparent', 'Hard'],
        correctAnswer: 'Transparent',
        explanation: 'Transparent materials allow light to pass through completely.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Lustre', back: 'Shine on the surface of materials'),
      Flashcard(front: 'Translucent', back: 'Allows light to pass partially')
    ],
    revisionNotes: 'Grouping helps in identifying and studying properties of materials.',
    commonMistakes: const ['Confusing translucent with transparent'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn Handpicking, Winnowing, and Sieving',
      'Understand Sedimentation, Decantation, and Filtration',
      'Process of Evaporation and Condensation'
    ],
    examples: const ['Separating tea leaves', 'Getting salt from sea water'],
    misconceptions: const ['Filtration can remove dissolved salt (only evaporation can)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'The process of conversion of water vapour into its liquid form is?',
        hint: 'Opposite of evaporation.',
        options: const ['Sedimentation', 'Condensation', 'Filtration', 'Winnowing'],
        correctAnswer: 'Condensation',
        explanation: 'Condensation is how clouds turn into rain.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Winnowing', back: 'Separating heavier and lighter components by wind'),
      Flashcard(front: 'Saturated Solution', back: 'No more solute can be dissolved at that temperature')
    ],
    revisionNotes: 'More than one method may be needed to separate a mixture.',
    commonMistakes: const ['Confusing decantation with sedimentation'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c4': ConceptNode(
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
    prerequisites: const ['e5_c5'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Classify: Herbs, Shrubs, Trees, Creepers, Climbers',
      'Functions of Stem, Leaf (Venation), and Root (Tap/Fibrous)',
      'Parts of a Flower (Sepals, Petals, Stamens, Pistil)'
    ],
    examples: const ['Parallel venation in grass', 'Reticulate venation in peepal'],
    misconceptions: const ['Plants only get food from soil (they make it via photosynthesis)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which part of the plant is responsible for Transpiration?',
        hint: 'It happens through stomata.',
        options: const ['Stem', 'Root', 'Leaf', 'Flower'],
        correctAnswer: 'Leaf',
        explanation: 'Water comes out of leaves in the form of vapour by transpiration.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Pistil', back: 'Innermost part of a flower (Female)'),
      Flashcard(front: 'Tap Root', back: 'Main root with smaller lateral roots')
    ],
    revisionNotes: 'Plants are the primary producers. Leaves are the "kitchen" of the plant.',
    commonMistakes: const ['Confusing Stamens with Pistils'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c5': ConceptNode(
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
    prerequisites: const ['e5_c1'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Types of joints: Ball and Socket, Pivotal, Hinge, Fixed',
      'Understand the human skeleton and X-rays',
      'Gait of animals (Earthworm, Snail, Cockroach, Fish, Bird)'
    ],
    examples: const ['Shoulder joint (Ball and socket)', 'Knee joint (Hinge)'],
    misconceptions: const ['Bones are not living (they are living tissues)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which joint allows movement in all directions?',
        hint: 'Think of your shoulder.',
        options: const ['Hinge joint', 'Fixed joint', 'Ball and socket joint', 'Pivotal joint'],
        correctAnswer: 'Ball and socket joint',
        explanation: 'It allows the maximum range of motion.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Cartilage', back: 'Soft parts of skeleton (e.g. ear lobe)'),
      Flashcard(front: 'Rib Cage', back: 'Protects the heart and lungs')
    ],
    revisionNotes: 'Muscles work in pairs - one contracts while the other relaxes.',
    commonMistakes: const ['Thinking snakes have no bones (they have a long backbone)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Biotic and Abiotic components',
      'Adaptations in Desert, Mountain, and Marine habitats',
      'Common characteristics of living beings'
    ],
    examples: const ['Cactus has spines for leaves', 'Snow leopards have thick fur'],
    misconceptions: const ['Acclimatization is same as Adaptation (acclimatization is short-term)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which of these is an abiotic component?',
        hint: 'It is a non-living thing.',
        options: const ['Plants', 'Animals', 'Soil', 'Bacteria'],
        correctAnswer: 'Soil',
        explanation: 'Abiotic components include non-living things like rocks, soil, air, and water.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Adaptation', back: 'Presence of specific features to live in a habitat'),
      Flashcard(front: 'Excretion', back: 'Getting rid of waste by living organisms')
    ],
    revisionNotes: 'Living things respond to stimuli, grow, and reproduce.',
    commonMistakes: const ['Thinking all aquatic animals have gills (Dolphins/Whales have blowholes)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c7': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Evolution of transport',
      'Standard units of measurement (SI units)',
      'Types of motion: Rectilinear, Circular, Periodic'
    ],
    examples: const ['1 metre = 100 cm', 'Motion of a swing (Periodic)'],
    misconceptions: const ['Handspan is a standard unit of measurement'],
    practiceExercises: const [
      PracticeExercise(
        question: 'The motion of a spinning top is an example of?',
        hint: 'It moves around an axis.',
        options: const ['Rectilinear', 'Circular', 'Periodic', 'Random'],
        correctAnswer: 'Circular',
        explanation: 'An object moving in a circle or around an axis shows circular motion.'
      )
    ],
    flashcards: const [
      Flashcard(front: '1 km', back: '1000 metres'),
      Flashcard(front: 'Rectilinear', back: 'Motion in a straight line')
    ],
    revisionNotes: 'Use standard units to avoid confusion in measurements.',
    commonMistakes: const ['Measuring from the end of the ruler instead of 0 mark'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'How shadows are formed',
      'Difference between Image and Shadow',
      'Reflection from a mirror and Pinhole Camera'
    ],
    examples: const ['Moon is a non-luminous object', 'Shadows are always black'],
    misconceptions: const ['Shadows show the color of the object'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is required for a shadow to form?',
        hint: 'You need light and something that blocks it.',
        options: const ['Light only', 'Screen only', 'Opaque object only', 'Light, Opaque object, and Screen'],
        correctAnswer: 'Light, Opaque object, and Screen',
        explanation: 'All three are necessary to see a shadow.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Luminous', back: 'Objects that emit their own light (e.g. Sun)'),
      Flashcard(front: 'Reflection', back: 'Bouncing back of light from a surface')
    ],
    revisionNotes: 'Light travels in a straight line.',
    commonMistakes: const ['Thinking non-luminous objects cannot be seen'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c9': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand components of a simple circuit',
      'Identify Conductors and Insulators',
      'Function of a switch and an electric cell'
    ],
    examples: const ['Copper is a conductor', 'Rubber is an insulator'],
    misconceptions: const ['Electricity flows even if the circuit is open'],
    practiceExercises: const [
      PracticeExercise(
        question: 'A device that breaks the circuit is called?',
        hint: 'You use it to turn lights on/off.',
        options: const ['Battery', 'Switch', 'Bulb', 'Wire'],
        correctAnswer: 'Switch',
        explanation: 'A switch is a simple device that either breaks the circuit or completes it.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Filament', back: 'Tiny wire in a bulb that glows'),
      Flashcard(front: 'Terminals', back: 'Positive (+) and Negative (-) ends of a cell')
    ],
    revisionNotes: 'Electricity flows from positive to negative terminal.',
    commonMistakes: const ['Touching electric wires with wet hands'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c10': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Magnetic and non-magnetic materials',
      'Identify poles of a magnet',
      'Making your own magnet and magnetic compass'
    ],
    examples: const ['Compass points North-South', 'Iron is magnetic'],
    misconceptions: const ['Magnets can attract all metals (they don\'t attract Gold/Silver)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where is the attraction of a magnet strongest?',
        hint: 'At the ends.',
        options: const ['Middle', 'North Pole only', 'Both Poles', 'Everywhere'],
        correctAnswer: 'Both Poles',
        explanation: 'Magnetic force is most concentrated at the North and South poles.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Repulsion', back: 'Similar poles push each other away'),
      Flashcard(front: 'Attraction', back: 'Opposite poles pull each other')
    ],
    revisionNotes: 'A freely suspended magnet always rests in N-S direction.',
    commonMistakes: const ['Storing magnets incorrectly (leading to loss of magnetism)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  's6_c11': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Composition of Air (Nitrogen, Oxygen, etc.)',
      'Importance of the Atmosphere',
      'Availability of Oxygen to aquatic animals'
    ],
    examples: const ['Windmill generating power', 'Breathing under water'],
    misconceptions: const ['Air is empty space (it has mass and occupies space)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which gas is highest in percentage in our atmosphere?',
        hint: 'It is about 78%.',
        options: const ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Argon'],
        correctAnswer: 'Nitrogen',
        explanation: 'Nitrogen makes up the majority of our air.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Atmosphere', back: 'Layer of air surrounding the earth'),
      Flashcard(front: 'Oxygen', back: 'Gas required for burning and breathing')
    ],
    revisionNotes: 'Air is essential for life on Earth. Plants and animals maintain balance of gases.',
    commonMistakes: const ['Thinking air has only one gas'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 6 SOCIAL SCIENCE (Civics - Social and Political Life - I)
  // ===========================================================================

  'ss6_c1': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the concept of diversity',
      'Learn about diversity in Ladakh and Kerala',
      'Unity in Diversity (Nehru\'s phrase)'
    ],
    examples: const ['Different food, languages, religions', 'Story of Samir Ek and Samir Do'],
    misconceptions: const ['Diversity means inequality (diversity is difference, inequality is unfairness)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who coined the phrase "Unity in Diversity"?',
        hint: 'He was India\'s first Prime Minister.',
        options: const ['Gandhiji', 'Ambedkar', 'Jawaharlal Nehru', 'Sardar Patel'],
        correctAnswer: 'Jawaharlal Nehru',
        explanation: 'Nehru wrote about India\'s unity in his book "The Discovery of India".'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Ladakh Trade', back: 'Pashmina wool and Silk route connection'),
      Flashcard(front: 'Kerala Spices', back: 'Pepper, Cloves, Cardamoms')
    ],
    revisionNotes: 'India\'s diversity is its strength.',
    commonMistakes: const ['Thinking diversity only means religion'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c2': ConceptNode(
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
    prerequisites: const ['e5_c16'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Difference between Prejudice and Stereotype',
      'Impact of discrimination on people\'s lives',
      'Constitutional fight for equality (Dr. Ambedkar)'
    ],
    examples: const ['Stereotype: Boys don\'t cry', 'Prejudice: Negative opinions about rural people'],
    misconceptions: const ['Stereotypes are always true'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is known as the Father of the Indian Constitution?',
        hint: 'He fought for Dalit rights.',
        options: const ['Gandhiji', 'Dr. B.R. Ambedkar', 'Nehru', 'Radhakrishnan'],
        correctAnswer: 'Dr. B.R. Ambedkar',
        explanation: 'Ambedkar chaired the drafting committee and worked for equality.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Stereotype', back: 'Fixing people into one image based on group'),
      Flashcard(front: 'Discrimination', back: 'Acting on prejudices and treating people unfairly')
    ],
    revisionNotes: 'Equality is a value that we have to keep striving for.',
    commonMistakes: const ['Confusing Prejudice with Discrimination'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Functions of the government',
      'Levels of government: Local, State, National',
      'Types: Democracy and Monarchy'
    ],
    examples: const ['Building roads', 'Printing currency', 'Elections'],
    misconceptions: const ['Government is only the police (it includes all administrative bodies)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is a "Representative Democracy"?',
        hint: 'People choose their leaders.',
        options: const ['King rules', 'People vote for representatives', 'Direct rule by people', 'Army rule'],
        correctAnswer: 'People vote for representatives',
        explanation: 'In most modern democracies, people don\'t rule directly but choose reps.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Suffrage', back: 'The right to vote in elections'),
      Flashcard(front: 'Monarchy', back: 'Rule by a King or Queen with final decision power')
    ],
    revisionNotes: 'Government makes laws and everyone living in the country has to follow them.',
    commonMistakes: const ['Thinking state government handles national borders'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c4': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'People\'s participation in governance',
      'Resolving conflicts and promoting equality',
      'South Africa\'s struggle against Apartheid'
    ],
    examples: const ['Rallies, protests, signature campaigns', 'Nelson Mandela'],
    misconceptions: const ['Voting once is the only form of participation'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What was the policy of "Apartheid" in South Africa?',
        hint: 'Separation based on race.',
        options: const ['Equality for all', 'Separation of races', 'Free education', 'Animal rights'],
        correctAnswer: 'Separation of races',
        explanation: 'Apartheid meant separation on the basis of race (Blacks, Whites, Indians, etc.).'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Conflict', back: 'When people of different groups don\'t agree'),
      Flashcard(front: 'ANC', back: 'African National Congress')
    ],
    revisionNotes: 'A democracy resolves conflicts through laws and discussions.',
    commonMistakes: const ['Thinking all conflicts are bad for democracy'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c5': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Functioning of Gram Sabha and Gram Panchayat',
      'Sources of funds for Panchayats',
      'Three levels of Panchayats (Gram, Block, Zila)'
    ],
    examples: const ['Village water problems', 'BPL list approval'],
    misconceptions: const ['Gram Sabha and Gram Panchayat are the same (Sabha is the assembly of all adults)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is the head of the Gram Panchayat?',
        hint: 'He is elected by members.',
        options: const ['Collector', 'Sarpanch', 'Secretary', 'BDO'],
        correctAnswer: 'Sarpanch',
        explanation: 'The Panchayat members (Panches) elect a Sarpanch as the head.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Gram Sabha', back: 'Meeting of all adults who live in the area'),
      Flashcard(front: 'Zila Parishad', back: 'District level of the Panchayat system')
    ],
    revisionNotes: 'Panchayati Raj is the first tier of democratic government.',
    commonMistakes: const ['Confusing the Secretary (govt appointed) with Sarpanch (elected)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Role of a Police Station (FIR)',
      'Maintenance of Land Records (Patwari)',
      'Hindu Succession Amendment Act 2005'
    ],
    examples: const ['A dispute over a land boundary', 'Getting a copy of land map'],
    misconceptions: const ['Only sons inherit father\'s property (laws have changed!)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the person in charge of a Police Station called?',
        hint: 'Abbreviation is S.H.O.',
        options: const ['Patwari', 'Collector', 'Station House Officer', 'Jailor'],
        correctAnswer: 'Station House Officer',
        explanation: 'The SHO is the head of the local police station.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Patwari', back: 'Officer who measures land and keeps records'),
      Flashcard(front: 'Khasra', back: 'Register of land records kept by Patwari')
    ],
    revisionNotes: 'Patwari is also known as Lekhpal, Kanungo, or Village Officer in different states.',
    commonMistakes: const ['Thinking the Collector does the day-to-day land measuring'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c7': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Role of Ward Councillors and Committees',
      'Functions of the Municipal Corporation/Council',
      'Waste management and cleanliness in cities'
    ],
    examples: const ['Surat plague and cleanliness drive', 'Replaced street lights'],
    misconceptions: const ['Ward Councillors are appointed by government (they are elected)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is the head of a Municipal Corporation?',
        hint: 'It starts with M.',
        options: const ['Chairman', 'Mayor', 'Collector', 'Commissioner'],
        correctAnswer: 'Mayor',
        explanation: 'Large cities have a Mayor as the ceremonial head of the Corporation.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Municipal Commissioner', back: 'Officer who implements decisions (appointed)'),
      Flashcard(front: 'Ward', back: 'Division of a city for election purposes')
    ],
    revisionNotes: 'Property taxes provide money for city maintenance.',
    commonMistakes: const ['Confusing Municipal Council (small towns) with Corporation (cities)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c8': ConceptNode(
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
    prerequisites: const ['e5_c19'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Types of work in villages (Agricultural and Non-farming)',
      'Problems of small farmers and debt',
      'Life of landless laborers (Thulasi\'s story)'
    ],
    examples: const ['Terrace farming in Nagaland', 'Fishing in coastal villages'],
    misconceptions: const ['All villagers are farmers'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the main reason for farmer suicide in some regions?',
        hint: 'It involves borrowed money.',
        options: const ['Bad weather', 'Debt/Loan burden', 'Lack of seeds', 'Laziness'],
        correctAnswer: 'Debt/Loan burden',
        explanation: 'Small farmers often take loans and if the crop fails, they fall into a debt trap.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Terrace Farming', back: 'Farming on carved steps on mountain slopes'),
      Flashcard(front: 'Paddy', back: 'Rice crop')
    ],
    revisionNotes: '40% of rural families in India are agricultural laborers.',
    commonMistakes: const ['Thinking big farmers do all the manual work themselves'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_c9': ConceptNode(
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
    prerequisites: const ['e5_c22'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Self-employed workers on streets (vendors)',
      'Work in factories and casual labor',
      'Permanent vs Temporary jobs'
    ],
    examples: const ['Call center workers', 'Rickshaw pullers', 'Marketing managers'],
    misconceptions: const ['Street vendors don\'t contribute to economy'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which of these is a "Permanent Job"?',
        hint: 'It has benefits like PF and holidays.',
        options: const ['Daily wage laborer', 'Street vendor', 'Bank employee', 'Casual painter'],
        correctAnswer: 'Bank employee',
        explanation: 'Permanent jobs provide job security and benefits like health insurance.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Call Center', back: 'Centralized office that handles high volume of calls'),
      Flashcard(front: 'Labour Chowk', back: 'Place where daily wage workers wait for work')
    ],
    revisionNotes: 'Cities provide many opportunities but also many challenges for workers.',
    commonMistakes: const ['Thinking all office jobs are permanent'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 6 ENGLISH (Honeysuckle)
  // ===========================================================================

  'en6_c1': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn the value of hard work and self-help',
      'Understand the difference between a house (structure) and a home (family)',
      'Vocabulary: Britches, Elf, Glitch'
    ],
    examples: const ['Patrick being lazy', 'The little elf "helping" him', 'Family love in a home'],
    misconceptions: const ['The elf did all the work (Patrick actually did it while helping the elf)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What did Patrick think his cat was playing with?',
        hint: 'It was a tiny person.',
        options: const ['A ball', 'A little doll', 'A mouse', 'A piece of cloth'],
        correctAnswer: 'A little doll',
        explanation: 'Patrick thought it was a doll, but it was actually a man of the tiniest size (an elf).'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Ignoramus', back: 'An ignorant person who lacks education'),
      Flashcard(front: 'A Home is made of?', back: 'Unselfish acts, brothers, sisters, fathers, mothers')
    ],
    revisionNotes: 'Self-help is the best help. Patrick changed his attitude towards work.',
    commonMistakes: const ['Confusing "house" and "home" definitions'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c2': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Narrative of animal domestication (folklore)',
      'Appreciate the movement and beauty of a kite',
      'Vocabulary: Kinsman, Snort, Panic'
    ],
    examples: const ['Dog following Wolf, Bear, Lion', 'Dog finally choosing Man', 'A new kite snapping on a string'],
    misconceptions: const ['Dogs were always pets (they were once wild)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why did the dog finally choose Man as his master?',
        hint: 'The Lion was afraid of Man.',
        options: const ['Man is kind', 'Man is the strongest', 'Man has food', 'Man is fast'],
        correctAnswer: 'Man is the strongest',
        explanation: 'The dog wanted a master who was the strongest on earth, and he saw even the Lion feared Man.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Kinsman', back: 'A relative'),
      Flashcard(front: 'Raggeder', back: 'More torn or worn out (like a stuck kite)')
    ],
    revisionNotes: 'The dog found man to be the most powerful master. A kite looks bright when new.',
    commonMistakes: const ['Confusing the order of masters the dog tried'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Japanese folklore and rewards for virtue',
      'Understand the nature of sibling quarrels',
      'Vocabulary: Sake, Chopped, Mutters'
    ],
    examples: const ['Magic waterfall giving Sake to Taro', 'Waterfall giving plain water to greedy neighbors'],
    misconceptions: const ['Quarrels always have a clear reason (sometimes we don\'t even know why they start!)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What did the waterfall give to Taro?',
        hint: 'A delicious Japanese drink.',
        options: const ['Cold water', 'Hot tea', 'Delicious Sake', 'Milk'],
        correctAnswer: 'Delicious Sake',
        explanation: 'Because Taro was a thoughtful son, the magic waterfall gave him Sake.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Sake', back: 'A popular Japanese drink'),
      Flashcard(front: 'Quarrel outcome', back: 'The afternoon turned black, but they made up by night')
    ],
    revisionNotes: 'Kindness and devotion to parents are always rewarded.',
    commonMistakes: const ['Thinking Taro was greedy'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c4': ConceptNode(
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
    prerequisites: const ['e5_c11'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Life and achievements of Kalpana Chawla',
      'Understand that beauty is internal and in deeds',
      'Vocabulary: Astronaut, Space shuttle, Disaster'
    ],
    examples: const ['Columbia space shuttle', 'Beauty in the corn growing and people working'],
    misconceptions: const ['Kalpana was born in the USA (she was born in Karnal, India)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'In which year did the Columbia disaster happen?',
        hint: 'It was early 2000s.',
        options: const ['1997', '2003', '2005', '2001'],
        correctAnswer: '2003',
        explanation: 'Space Shuttle Columbia broke apart on 1st Feb 2003.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Space Shuttle', back: 'Spacecraft used for repeated journeys between Earth and station'),
      Flashcard(front: 'Beauty is heard in?', back: 'Wind sighing, rain falling, or a singer chanting')
    ],
    revisionNotes: 'Nothing is impossible if you have a dream and the courage to follow it.',
    commonMistakes: const ['Spelling of "Columbia"'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c5': ConceptNode(
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
    prerequisites: const ['h5_c9'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn the value of "blind day" and "dumb day" to feel empathy',
      'Understand a child\'s curiosity about teachers\' personal lives',
      'Vocabulary: Ghastly, Misfortune, Crutch'
    ],
    examples: const ['Miss Beam\'s school', 'Children with bandaged eyes'],
    misconceptions: const ['The children were actually disabled (they were practicing being disabled for a day)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What was the main aim of Miss Beam\'s school?',
        hint: 'It wasn\'t just about math or science.',
        options: const ['To make athletes', 'To teach thoughtfullness and kindness', 'To win awards', 'To be strict'],
        correctAnswer: 'To teach thoughtfullness and kindness',
        explanation: 'She wanted children to be "responsible citizens" who understand others\' pain.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Empathy', back: 'Understanding and sharing the feelings of another'),
      Flashcard(front: 'The poem\'s theme', back: 'Child\'s wonder if teachers are ordinary people too')
    ],
    revisionNotes: 'Experiencing a problem helps us respect those who live with it every day.',
    commonMistakes: const ['Thinking the school was cruel'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Appreciate diversity in human interests and dreams',
      'Understand the power of words and language',
      'Vocabulary: Rafting, Preserved, Marvel'
    ],
    examples: const ['Radha (climbing trees)', 'Peter (movies)', 'Language as the "dress of thought"'],
    misconceptions: const ['Words are just sounds (they are the only way to release thoughts)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who wants to be a "seed collector"?',
        hint: 'A boy in the chapter.',
        options: const ['Nasir', 'Rohit', 'Peter', 'Dolma'],
        correctAnswer: 'Nasir',
        explanation: 'Nasir wants to learn how to preserve seeds to help his grandfather.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Language', back: 'The dress of thought'),
      Flashcard(front: 'Dolma\'s dream', back: 'To be the Prime Minister of India')
    ],
    revisionNotes: 'Everyone is unique with different strengths and goals.',
    commonMistakes: const ['Mixing up the children\'s names and their dreams'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c7': ConceptNode(
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
    prerequisites: const ['ss6_c5'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the role of the Panchayat in villages',
      'The principle that "The Voice of the Panch is the Voice of God"',
      'Vocabulary: Property, Culprit, Reluctant'
    ],
    examples: const ['Jumman Sheikh and Algu Chowdhury', 'The aunt\'s case'],
    misconceptions: const ['Friends should support each other even in wrong acts'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who was appointed as the Head Panch by the aunt?',
        hint: 'Jumman\'s best friend.',
        options: const ['Jumman', 'Algu Chowdhury', 'Samjhu Sahu', 'The Village Head'],
        correctAnswer: 'Algu Chowdhury',
        explanation: 'The aunt chose Algu, trusting his honesty despite his friendship with Jumman.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Panchayat', back: 'A village council that settles disputes'),
      Flashcard(front: 'Moral of Fair Play', back: 'Justice should come before friendship')
    ],
    revisionNotes: 'A person on the seat of a judge has no friend or enemy, only the truth.',
    commonMistakes: const ['Thinking Algu was mean to Jumman'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about fair ground tricks and luck',
      'Appreciate different vocations (Hawker, Gardener, Watchman)',
      'Vocabulary: Disappointed, Trifle, Chasing'
    ],
    examples: const ['Lucky Shop at the Eid fair', 'Rashid losing money', 'Child wishing to be a watchman'],
    misconceptions: const ['"Game of Chance" shops are honest (they are often fixed to trick people)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why was Rashid upset after the fair?',
        hint: 'He played the Lucky Shop.',
        options: const ['He lost his way', 'He lost all his money', 'He didn\'t get a toy', 'His uncle scolded him'],
        correctAnswer: 'He lost all his money',
        explanation: 'He was tricked into thinking he was unlucky, while the shopkeeper was cheating.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Vocation', back: 'A person\'s trade or profession'),
      Flashcard(front: 'Gong', back: 'A metal disk that makes a sound when struck')
    ],
    revisionNotes: 'Don\'t be fooled by the lure of easy money. Every job has its own life.',
    commonMistakes: const ['Confusing the vocations in the poem'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c9': ConceptNode(
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
    prerequisites: const ['s6_c6'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn how animals survive in deserts (Camels, Snakes, Gerbils)',
      'Handle "What if" anxious thoughts',
      'Vocabulary: Dunes, Scorching, Slither'
    ],
    examples: const ['Rattlesnake warning', 'Camel\'s humps (storing fat, not water)'],
    misconceptions: const ['Camels store water in their humps (it is fat!)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'How many litres of water can a thirsty camel drink in ten minutes?',
        hint: 'It is a huge amount.',
        options: const ['10 litres', '30 litres', '100 litres', '50 litres'],
        correctAnswer: '100 litres',
        explanation: 'A camel can drink about 30 gallons (100 litres) in just 10 mins.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Gila Monster', back: 'A poisonous lizard found in American deserts'),
      Flashcard(front: 'Whatif thoughts', back: 'Anxious worries that come at night')
    ],
    revisionNotes: 'Deserts are not just sand; they have a rich variety of life. Everyone has worries.',
    commonMistakes: const ['Thinking snakes can hear (they feel vibrations)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'en6_c10': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about the ecosystem of a banyan tree',
      'Classic battle between Cobra and Mongoose',
      'Vocabulary: Prop, Magnificence, Aggressive'
    ],
    examples: const ['Squirrels and birds in the tree', 'The grey mongoose vs black cobra'],
    misconceptions: const ['The mongoose is immune to snake venom (it is just very fast)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who were the two "uninvited" spectators of the fight?',
        hint: 'A bird and an animal.',
        options: const ['Myna and Crow', 'Cat and Dog', 'Parrot and Eagle', 'Owl and Rat'],
        correctAnswer: 'Myna and Crow',
        explanation: 'A myna and a jungle crow sat on a cactus to watch the battle.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Banyan tree age', back: 'Older than the house, as old as the town'),
      Flashcard(front: 'Mongoose weapon', back: 'Speed and agility')
    ],
    revisionNotes: 'Nature has its own laws of survival. The banyan tree is a world in itself.',
    commonMistakes: const ['Thinking the crow survived the fight (it was bitten by the cobra)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 6 HINDI (Vasant)
  // ===========================================================================

  'h6_c1': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the desire for freedom through a bird',
      'Appreciate the beauty of nature and rivers',
      'Vocabulary: Santoshi, Garvili, Jundi'
    ],
    examples: const ['Bird eating Jundi grains', 'Bird drinking from the overflowing river'],
    misconceptions: const ['The bird is real (it is a symbol of human qualities like self-respect)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which river is mentioned in the poem?',
        hint: 'The bird drinks water from it.',
        options: const ['Ganga', 'Yamuna', 'Chadhi Nadi', 'Narmada'],
        correctAnswer: 'Chadhi Nadi',
        explanation: 'The poet uses "Chadhi Nadi" to describe an overflowing, powerful river.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Santoshi', back: 'Contented / Satisfied'),
      Flashcard(front: 'Garvili', back: 'Proud (in a positive way)')
    ],
    revisionNotes: 'The poem emphasizes contentment and love for freedom.',
    commonMistakes: const ['Thinking the bird is a specific species'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c2': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Recall childhood memories (Krishna Sobti)',
      'Compare old times with modern times',
      'Vocabulary: Siyahi, Shani-Ravivar, Gramophone'
    ],
    examples: const ['Drinking castor oil on Sundays', 'First time wearing spectacles'],
    misconceptions: const ['Old times were boring without mobile phones'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What did the author have to drink every Sunday morning?',
        hint: 'It was for health.',
        options: const ['Milk', 'Castor Oil', 'Juice', 'Tea'],
        correctAnswer: 'Castor Oil',
        explanation: 'The author mentions taking olive oil or castor oil for health on Sundays.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Gramophone', back: 'An old device used for playing music'),
      Flashcard(front: 'Convent School', back: 'Type of school mentioned in memories')
    ],
    revisionNotes: 'Lifestyles change with time, but childhood joys remain universal.',
    commonMistakes: const ['Thinking the author is a man'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the curiosity of children towards nature',
      'Learn about animal behavior (birds and eggs)',
      'Moral lesson on unintended harm'
    ],
    examples: const ['Keshav and Shyama', 'Cornice of the house'],
    misconceptions: const ['Birds will be happy if we provide them a bed/cushion (they might desert the eggs if humans touch them)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Why did the bird break her own eggs?',
        hint: 'Humans touched them.',
        options: const ['They were bad', 'Because they became dirty (human touch)', 'By mistake', 'To eat them'],
        correctAnswer: 'Because they became dirty (human touch)',
        explanation: 'Once humans touch bird eggs, the mother often leaves or breaks them.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Nadan', back: 'Innocent / Foolish'),
      Flashcard(front: 'Cornice', back: 'A horizontal decorative molding')
    ],
    revisionNotes: 'Love for animals should be combined with knowledge of their nature.',
    commonMistakes: const ['Thinking Keshav was mean to the birds'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c4': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Enjoy the whimsical imagination of a child',
      'Learn about the phases of the moon in poetic language',
      'Vocabulary: Akas, Kul, Tirchi'
    ],
    examples: const ['Stars as a dress for the moon', 'Moon growing and shrinking as a disease'],
    misconceptions: const ['The moon is actually sick (it is just a child\'s perspective)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What does the child think the moon\'s "dress" is made of?',
        hint: 'Look at the night sky.',
        options: const ['Cloud', 'Stars', 'Silk', 'Silver'],
        correctAnswer: 'Stars',
        explanation: 'The child imagines the moon wearing the entire sky studded with stars.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Akas', back: 'Sky'),
      Flashcard(front: 'Kul', back: 'Total / Entire')
    ],
    revisionNotes: 'Poetry allows us to see common things in extraordinary ways.',
    commonMistakes: const ['Mixing up the waxing and waning phases'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c5': ConceptNode(
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
    prerequisites: const ['ss6_h1'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the importance of letters and script',
      'History of human communication',
      'Difference between Prehistory and History'
    ],
    examples: const ['Ideograms (picture signs)', 'Discovery of writing 6000 years ago'],
    misconceptions: const ['Letters were created by God (they were invented by humans)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'When did the history of mankind begin?',
        hint: 'When we started writing.',
        options: const ['1 million years ago', 'When letters were invented', 'When fire was discovered', 'With the wheel'],
        correctAnswer: 'When letters were invented',
        explanation: 'History begins when we can read what people wrote in the past.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Pragaitihasik', back: 'Prehistoric (before written records)'),
      Flashcard(front: 'Lipya', back: 'Scripts')
    ],
    revisionNotes: 'Writing allowed humans to store knowledge and pass it to generations.',
    commonMistakes: const ['Thinking alphabets were always there'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Explore the genre of science fiction',
      'Imagining underground life on Mars',
      'Handling curiosity and rules'
    ],
    examples: const ['Chhotu using father\'s security card', 'Viking mission to Mars'],
    misconceptions: const ['Mars is currently inhabited by underground people'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where did Chhotu\'s family live?',
        hint: 'It was for protection from the surface.',
        options: const ['In a forest', 'Under the surface of Mars', 'On the Moon', 'In a city like Delhi'],
        correctAnswer: 'Under the surface of Mars',
        explanation: 'In the story, life on the surface became impossible, so they moved underground.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Yantra', back: 'Machine / Instrument'),
      Flashcard(front: 'Viking', back: 'Real-life NASA mission to Mars mentioned in the chapter')
    ],
    revisionNotes: 'Science fiction combines scientific facts with imaginative storytelling.',
    commonMistakes: const ['Confusing the fictional story with scientific reality'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c7': ConceptNode(
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
    prerequisites: const ['en5_c2'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Value of collective effort',
      'Inspiration for hard-working people',
      'Hindi vocabulary related to strength'
    ],
    examples: const ['Building a road together', 'Turning mountains into paths'],
    misconceptions: const ['One hero does everything alone'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is the poet of "Sathi Hath Badhana"?',
        hint: 'A famous lyricist.',
        options: const ['Sahir Ludhianvi', 'Gulzar', 'Javed Akhtar', 'Bachchan'],
        correctAnswer: 'Sahir Ludhianvi',
        explanation: 'This inspiring song/poem was written by Sahir Ludhianvi.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Fauladi', back: 'Made of steel / Very strong'),
      Flashcard(front: 'Naseeb', back: 'Fate / Destiny')
    ],
    revisionNotes: 'Work becomes light and successful when everyone helps.',
    commonMistakes: const ['Thinking the poem is only for laborers'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Humorous take on children\'s fear of homework',
      'Structure of a one-act play (Ekanki)',
      'Understanding character roles'
    ],
    examples: const ['Mohan pretending to have a stomach ache', 'The Doctor and Vaidya visiting'],
    misconceptions: const ['Mohan had a real illness'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What was the "Aise-Aise" disease?',
        hint: 'It wasn\'t real.',
        options: const ['Stomach flu', 'Fear of homework', 'Headache', 'Fever'],
        correctAnswer: 'Fear of homework',
        explanation: 'Mohan didn\'t finish his school work, so he made an excuse using "Aise-Aise".'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Ekanki', back: 'A one-act play'),
      Flashcard(front: 'Vaidya Ji', back: 'Traditional Indian doctor')
    ],
    revisionNotes: 'Honesty with teachers and parents avoids unnecessary drama.',
    commonMistakes: const ['Missing the comic timing of the play'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c9': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the feeling of jealousy and regret',
      'Learn about the hobby of philately (stamp collecting)',
      'Moral value of confession and honesty'
    ],
    examples: const ['Rajappa burning Nagarajan\'s album', 'Rajappa giving his own album in the end'],
    misconceptions: const ['Rajappa was a "bad" person (he was just overwhelmed by envy)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who got a ticket album from Singapore?',
        hint: 'The popular boy.',
        options: const ['Rajappa', 'Nagarajan', 'Krishna', 'Appu'],
        correctAnswer: 'Nagarajan',
        explanation: 'Nagarajan\'s uncle sent him a beautiful album from Singapore.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Irshya', back: 'Jealousy / Envy'),
      Flashcard(front: 'Pashchatap', back: 'Regret / Remorse')
    ],
    revisionNotes: 'Envy can make a person do wrong things, but true courage lies in accepting mistakes.',
    commonMistakes: const ['Thinking Rajappa stole the album to sell it'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c10': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Biography of Laxmi Bai in verse',
      'Understand the 1857 revolt against British',
      'Vocabulary: Veer-gatha, Dalhousie, Inquilab'
    ],
    examples: const ['Laxmi Bai playing with dolls vs swords', 'Fighting like a man (Khoob ladi mardani)'],
    misconceptions: const ['Jhansi was the only state that fought (many fought, but Jhansi was legendary)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is the author of this poem?',
        hint: 'Same as "Khilaunewala".',
        options: const ['Mahadevi Verma', 'Subhadra Kumari Chauhan', 'Sarojini Naidu', 'Prasad'],
        correctAnswer: 'Subhadra Kumari Chauhan',
        explanation: 'Subhadra Kumari Chauhan wrote this famous patriotic poem.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Chhabili', back: 'Laxmi Bai\'s childhood name'),
      Flashcard(front: 'Birsingha', back: 'Bundelkhandi bard mentioned in poem')
    ],
    revisionNotes: 'The Queen of Jhansi was one of the greatest heroes of India\'s first war of independence.',
    commonMistakes: const ['Spelling of "Subhadra Kumari Chauhan"'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c11': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Understand the perspective of a visually impaired person (Helen Keller)',
      'Learn to appreciate nature using other senses',
      'Value of being grateful for our abilities'
    ],
    examples: const ['Feeling the texture of birch tree bark', 'Listening to bird songs'],
    misconceptions: const ['Blind people cannot enjoy the beauty of nature'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is the author of this essay?',
        hint: 'A world-famous deaf-blind author.',
        options: const ['Krishna Sobti', 'Helen Keller', 'Premchand', 'Tagore'],
        correctAnswer: 'Helen Keller',
        explanation: 'Helen Keller shares how she "sees" nature through touch and smell.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Anubhuti', back: 'Feeling / Experience'),
      Flashcard(front: 'Samvedna', back: 'Sensitivity / Empathy')
    ],
    revisionNotes: 'We often take our senses for granted, while those who lack them value them more.',
    commonMistakes: const ['Thinking Helen Keller was born deaf-blind (she became so after illness)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c12': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about Nehru\'s letters to his daughter Indira',
      'Nature as a giant book we should learn to read',
      'Formation of stones, pebbles, and sand'
    ],
    examples: const ['A small pebble tells a story of its long journey', 'Pebble becoming sand over time'],
    misconceptions: const ['Stones are just dead objects with no story'],
    practiceExercises: const [
      PracticeExercise(
        question: 'To whom did Jawaharlal Nehru write these letters?',
        hint: 'His daughter.',
        options: const ['Sonia', 'Indira Gandhi', 'Vijaya Lakshmi', 'Priyanka'],
        correctAnswer: 'Indira Gandhi',
        explanation: 'Nehru wrote these letters when Indira was 10 years old and in Mussoorie.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Ghor', back: 'Deep / Intense'),
      Flashcard(front: 'Kankad', back: 'Pebble')
    ],
    revisionNotes: 'The Earth is very old, and to understand its history, we must read the signs in nature.',
    commonMistakes: const ['Thinking these were formal academic articles'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c13': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Enjoy the sweet bond between mother and child',
      'Desire to remain small to never lose mother\'s proximity',
      'Vocabulary: Aanchal, Chhalna, Sneh'
    ],
    examples: const ['Holding mother\'s hand always', 'Listening to stories in mother\'s lap'],
    misconceptions: const ['The child hates growing up (it\'s just a metaphor for love)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who is the poet of "Main Sabse Chhoti Hun"?',
        hint: 'He is a famous Chhayavadi poet.',
        options: const ['Sumitranandan Pant', 'Nirala', 'Prasad', 'Verma'],
        correctAnswer: 'Sumitranandan Pant',
        explanation: 'Sumitranandan Pant wrote this beautiful poem about a child\'s love.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Aanchal', back: 'Corner of a sari / Mother\'s protection'),
      Flashcard(front: 'Nishhal', back: 'Pure / Innocent')
    ],
    revisionNotes: 'The poet expresses the purest form of love and dependence on a mother.',
    commonMistakes: const ['Misidentifying the poet'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c14': ConceptNode(
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
    prerequisites: const ['h5_c2'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about the diversity of Indian folk songs',
      'Instruments used in folk music (Dholak, Kartal)',
      'Social importance of community singing'
    ],
    examples: const ['Bidesiya (Bihar)', 'Baul (Bengal)', 'Garba (Gujarat)'],
    misconceptions: const ['Folk songs are only for villages (they are the soul of our culture)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which of these is a famous folk song of Bihar?',
        hint: 'It starts with B.',
        options: const ['Kajri', 'Bidesiya', 'Lavani', 'Bhangra'],
        correctAnswer: 'Bidesiya',
        explanation: 'Bidesiya is a very popular folk song in Bhojpuri speaking regions.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Shastriya Sangeet', back: 'Classical Music'),
      Flashcard(front: 'Heer-Ranjha', back: 'Folk songs of Punjab')
    ],
    revisionNotes: 'Folk songs are flexible and change with the people who sing them.',
    commonMistakes: const ['Thinking folk music needs expensive electronic instruments'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c15': ConceptNode(
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
    prerequisites: const ['e5_c16'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about Gandhiji\'s self-reliance',
      'Value of doing one\'s own work',
      'Respect for physical labor'
    ],
    examples: const ['Gandhiji grinding flour', 'Gandhiji cleaning toilets', 'Caring for guests'],
    misconceptions: const ['Leaders don\'t need to do manual work'],
    practiceExercises: const [
      PracticeExercise(
        question: 'In which ashram did Gandhiji set examples of self-work?',
        hint: 'Near Ahmedabad.',
        options: const ['Sabarmati Ashram', 'Sevagram', 'Both', 'None'],
        correctAnswer: 'Both',
        explanation: 'Gandhiji lived a simple life of labor in all his ashrams.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Svavalamban', back: 'Self-reliance'),
      Flashcard(front: 'Kasturba', back: 'Gandhiji\'s wife who supported him in simple life')
    ],
    revisionNotes: 'No work is low if done with devotion and honesty.',
    commonMistakes: const ['Thinking Gandhiji was forced to do this work'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'h6_c16': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Appreciate Tulsidas\'s Brajbhasha/Awadhi poetry',
      'Story of Ram, Sita, and Laxman going to exile',
      'Expressions of exhaustion and love'
    ],
    examples: const ['Sita getting tired after a few steps', 'Ram shedding tears seeing her state'],
    misconceptions: const ['Sita was weak (she was a princess who chose a difficult path for love)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who wrote the verses in "Van ke Marg Mein"?',
        hint: 'The author of Ramcharitmanas.',
        options: const ['Kabir', 'Surdas', 'Tulsidas', 'Raskhan'],
        correctAnswer: 'Tulsidas',
        explanation: 'Goswami Tulsidas composed these beautiful verses.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Savaiya', back: 'The poetic meter used in this chapter'),
      Flashcard(front: 'Kanya', back: 'Princess (Sita)')
    ],
    revisionNotes: 'The poem beautifully captures the initial hardships of the forest journey.',
    commonMistakes: const ['Thinking this is modern Hindi (it is older dialect)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h1': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about river valley civilizations (Narmada, Indus, Ganga)',
      'Difference between Manuscripts and Inscriptions',
      'Understand dates (BC/AD or BCE/CE)'
    ],
    examples: const ['Manuscripts on palm leaves', 'Inscriptions on stone/metal'],
    misconceptions: const ['History is only about Kings (it is about common people too)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where did people first start living near rivers in India?',
        hint: 'Narmada is one of them.',
        options: const ['Narmada valley', 'Thar desert', 'Himalayas', 'Deccan plateau'],
        correctAnswer: 'Narmada valley',
        explanation: 'People lived along the banks of Narmada for several hundred thousand years.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Manuscript', back: 'Books written by hand (Latin "Manu" means hand)'),
      Flashcard(front: 'Archaeologist', back: 'One who studies objects from the past')
    ],
    revisionNotes: 'History helps us understand how our ancestors lived.',
    commonMistakes: const ['Confusing AD with "After Death" (it is Anno Domini)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h2': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Lifestyle of hunter-gatherers',
      'Discovery of fire and its uses',
      'The transition to farming and herding'
    ],
    examples: const ['Bhimbetka caves (MP)', 'Mehrgarh (Pakistan)'],
    misconceptions: const ['Farming happened overnight (it was a gradual process over thousands of years)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'In which site was fire first evidence found?',
        hint: 'It is a cave site.',
        options: const ['Bhimbetka', 'Kurnool caves', 'Mehrgarh', 'Burzahom'],
        correctAnswer: 'Kurnool caves',
        explanation: 'Traces of ash have been found here, suggesting use of fire.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Domestication', back: 'Process of tending plants and animals for human use'),
      Flashcard(front: 'Burzahom', back: 'Site in Kashmir known for pit-houses')
    ],
    revisionNotes: 'Stone ages: Palaeolithic, Mesolithic, Neolithic.',
    commonMistakes: const ['Thinking hunter-gatherers lived in one place'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h3': ConceptNode(
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
    prerequisites: const ['e5_c10'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Unique features of Harappan cities (Citadel, Lower Town)',
      'Drainage system and urban planning',
      'Harappan crafts, trade, and mystery of decline'
    ],
    examples: const ['Great Bath in Mohenjodaro', 'Terracotta toys', 'Seals'],
    misconceptions: const ['Harappans had no writing system (they had a script, but it\'s undeciphered)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where was the "Great Bath" found?',
        hint: 'A major Harappan city.',
        options: const ['Harappa', 'Mohenjodaro', 'Lothal', 'Dholavira'],
        correctAnswer: 'Mohenjodaro',
        explanation: 'The Great Bath was a special tank lined with bricks and plaster.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Citadel', back: 'The higher, smaller western part of a Harappan city'),
      Flashcard(front: 'Lothal', back: 'Harappan city in Gujarat with a dockyard')
    ],
    revisionNotes: 'Harappan cities were famous for baked bricks and planned streets.',
    commonMistakes: const ['Confusing the Citadel with the Lower Town'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h4': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'About the four Vedas (Rigveda, Samaveda, Yajurveda, Atharvaveda)',
      'Social differences observed in burials',
      'Importance of Horses and Chariots in Vedic times'
    ],
    examples: const ['Megaliths at Inamgaon', 'Suktas (hymns)'],
    misconceptions: const ['Vedas were written down immediately (they were oral for centuries)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which is the oldest Veda?',
        hint: 'It has more than 1000 hymns.',
        options: const ['Rigveda', 'Samaveda', 'Yajurveda', 'Atharvaveda'],
        correctAnswer: 'Rigveda',
        explanation: 'The Rigveda was composed about 3500 years ago.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Megalith', back: 'Big stones used to mark burial sites'),
      Flashcard(front: 'Sanskrit', back: 'Part of the Indo-European language family')
    ],
    revisionNotes: 'Burials often contain objects that suggest the person\'s status.',
    commonMistakes: const ['Confusing Vedic culture with Harappan culture'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h5': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Process of becoming a Raja (Ashvamedha sacrifice)',
      'Life in Mahajanapadas (Magadha, Vajji)',
      'Taxation and changes in agriculture'
    ],
    examples: const ['Vajji Gana-sangha', 'The fortress of Magadha'],
    misconceptions: const ['All ancient kingdoms were monarchies (some were Ganas/Republics)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What was the capital of the Vajji gana?',
        hint: 'It is in present-day Bihar.',
        options: const ['Rajagriha', 'Pataliputra', 'Vaishali', 'Ujjain'],
        correctAnswer: 'Vaishali',
        explanation: 'Vaishali was the capital of the Vajji confederacy.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Ashvamedha', back: 'Horse sacrifice ritual to establish power'),
      Flashcard(front: 'Bhaga', back: 'Tax on crops (1/6th of produce)')
    ],
    revisionNotes: 'Magadha became powerful due to rivers, iron mines, and elephants.',
    commonMistakes: const ['Confusing Magadha with Vajji systems'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Story of Buddha and basic teachings',
      'Principles of Jainism (Lord Mahavira)',
      'Concepts of Atman and Brahman in Upanishads'
    ],
    examples: const ['Story of Kisagotami', 'Sarnath (first sermon)'],
    misconceptions: const ['Buddhism and Jainism were only for the rich'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where did the Buddha attain enlightenment?',
        hint: 'Under a Peepal tree.',
        options: const ['Lumbini', 'Sarnath', 'Bodh Gaya', 'Kushinagar'],
        correctAnswer: 'Bodh Gaya',
        explanation: 'Siddhartha Gautama became the Buddha at Bodh Gaya in Bihar.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Tanha', back: 'Desire or craving (Buddhism)'),
      Flashcard(front: 'Sangha', back: 'Association of those who left their homes')
    ],
    revisionNotes: 'Ahimsa (non-violence) is a core value of Jainism.',
    commonMistakes: const ['Confusing the birth place of Buddha with the enlightenment place'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h7': ConceptNode(
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
    prerequisites: const ['ss6_h5'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Founding of Mauryan Empire (Chandragupta Maurya)',
      'Impact of the Kalinga War',
      'Ashoka\'s Dhamma and its propagation'
    ],
    examples: const ['Edicts of Ashoka', 'Lion Capital at Sarnath'],
    misconceptions: const ['Dhamma is a new religion (it is a code of conduct)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which war changed Ashoka\'s heart?',
        hint: 'A bloody battle on the east coast.',
        options: const ['Battle of Panipat', 'Kalinga War', 'Battle of Plassey', 'Magadha War'],
        correctAnswer: 'Kalinga War',
        explanation: 'The suffering in Kalinga made Ashoka embrace peace and Dhamma.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Chanakya', back: 'Wise man who wrote Arthashastra'),
      Flashcard(front: 'Pataliputra', back: 'Capital of the Mauryan Empire')
    ],
    revisionNotes: 'Ashoka was the first ruler to communicate with people through edicts.',
    commonMistakes: const ['Thinking Ashoka was the founder of the empire'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Use of iron tools in agriculture',
      'Life in villages (Gramabhojaka, Grihapatis)',
      'Punch-marked coins and early trade centers (Arikamedu)'
    ],
    examples: const ['Ring wells', 'Northern Black Polished Ware (NBPW)'],
    misconceptions: const ['Cities didn\'t have sanitation (Ring wells were used for toilets/drains)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What were early coins called?',
        hint: 'Designs were hit onto the metal.',
        options: const ['Gold coins', 'Punch-marked coins', 'Rupees', 'Dinars'],
        correctAnswer: 'Punch-marked coins',
        explanation: 'They were generally rectangular or round with symbols punched on them.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Gramabhojaka', back: 'Village headman (North India)'),
      Flashcard(front: 'Shrenis', back: 'Associations of crafts persons and merchants')
    ],
    revisionNotes: 'Irrigation (canals, wells, tanks) boosted production.',
    commonMistakes: const ['Thinking everyone in villages owned land'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h9': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'The famous Silk Route and its control',
      'Spread of Buddhism (Mahayana) and statues',
      'Rise of Bhakti and foreign pilgrims (Fa-Xian, Xuan Zang)'
    ],
    examples: const ['Kushanas and Kanishka', 'Nalanda university'],
    misconceptions: const ['The Silk Route was only for silk'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which famous university did Xuan Zang visit in India?',
        hint: 'A great center of learning.',
        options: const ['Taxila', 'Nalanda', 'Vikramshila', 'Banaras'],
        correctAnswer: 'Nalanda',
        explanation: 'Nalanda was a world-famous Buddhist monastery and university.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Bhakti', back: 'Devotion to a chosen deity'),
      Flashcard(front: 'Bodhisattvas', back: 'Enlightened persons who stayed to help others')
    ],
    revisionNotes: 'Trade spread not just goods, but also ideas and religions.',
    commonMistakes: const ['Thinking Buddhism didn\'t change over time'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h10': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Learn about Samudragupta from Prashastis',
      'The Golden Age of Guptas (Harshavardhana)',
      'Kingdoms in the South (Pallavas and Chalukyas)'
    ],
    examples: const ['Allahabad Pillar inscription', 'Aihole inscription'],
    misconceptions: const ['Southern kingdoms were less organized than Northern ones'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Who was the court poet of Samudragupta?',
        hint: 'He wrote the Allahabad Prashasti.',
        options: const ['Kalidasa', 'Harishena', 'Banabhatta', 'Ravikirti'],
        correctAnswer: 'Harishena',
        explanation: 'Harishena wrote a long poem in praise of Samudragupta.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Prashasti', back: 'Sanskrit word meaning "in praise of"'),
      Flashcard(front: 'Dakshinapatha', back: 'Route to the south (12 rulers defeated by Samudragupta)')
    ],
    revisionNotes: 'Administrative systems became more decentralized during this period.',
    commonMistakes: const ['Confusing Harishena with Ravikirti (Chalukya poet)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_h11': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Metallurgy (Iron Pillar at Mehrauli)',
      'Architecture of Stupas and Temples',
      'Literature: Epics (Silappadikaram, Ramayana, Mahabharata)'
    ],
    examples: const ['Ajanta paintings', 'Aryabhatiyam by Aryabhata'],
    misconceptions: const ['Ancient Indians didn\'t know advanced science (Aryabhata knew Earth rotates!)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Where is the famous Iron Pillar located?',
        hint: 'Near the Qutub Minar in Delhi.',
        options: const ['Delhi', 'Mumbai', 'Agra', 'Patna'],
        correctAnswer: 'Delhi',
        explanation: 'The Iron Pillar at Mehrauli, Delhi, hasn\'t rusted in 1500 years!'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Aryabhata', back: 'Mathematician and Astronomer who explained eclipses'),
      Flashcard(front: 'Stupa', back: 'Relic casket (mound) containing Buddhist remains')
    ],
    revisionNotes: 'Stories were preserved through Puranas and Epics.',
    commonMistakes: const ['Thinking temples and stupas were built by one person alone'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  // ===========================================================================
  // CLASS 6 SOCIAL SCIENCE (Geography - The Earth: Our Habitat)
  // ===========================================================================

  'ss6_g1': ConceptNode(
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
    prerequisites: const ['e5_c11'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Define celestial bodies: Stars, Planets, Satellites',
      'Understand the Solar System components',
      'Unique features of Earth and Moon'
    ],
    examples: const ['Sun is a star', 'Earth is the Blue Planet'],
    misconceptions: const ['Stars are small (they are huge but very far away)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which is the third nearest planet to the Sun?',
        hint: 'It is our home.',
        options: const ['Venus', 'Mars', 'Earth', 'Jupiter'],
        correctAnswer: 'Earth',
        explanation: 'The order is Mercury, Venus, Earth...'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Galaxy', back: 'Huge system of billions of stars (e.g. Milky Way)'),
      Flashcard(front: 'Orbit', back: 'Fixed path on which planets move around Sun')
    ],
    revisionNotes: 'Earth is the only planet known to have life.',
    commonMistakes: const ['Thinking Pluto is still a planet (it is a dwarf planet)'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_g2': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Define Equator, Parallels of Latitudes',
      'Understand Meridians of Longitudes and Prime Meridian',
      'Relationship between Longitude and Time'
    ],
    examples: const ['IST (Indian Standard Time) is 82°30\'E', 'Equator is 0° latitude'],
    misconceptions: const ['Latitudes meet at the poles (Longitudes meet at poles, latitudes are parallel)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'What is the value of the Prime Meridian?',
        hint: 'It passes through Greenwich.',
        options: const ['90°', '0°', '180°', '60°'],
        correctAnswer: '0°',
        explanation: 'Prime Meridian is the starting point for Longitude.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Torrid Zone', back: 'Hottest zone between Tropics'),
      Flashcard(front: 'Grid', back: 'Network of latitudes and longitudes')
    ],
    revisionNotes: '1 degree of longitude = 4 minutes of time.',
    commonMistakes: const ['Confusing Latitudes with Longitudes'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_g3': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Difference between Rotation and Revolution',
      'Causes of Day and Night',
      'Causes of Seasons (Solstice and Equinox)'
    ],
    examples: const ['Leap year every 4 years', 'Christmas in summer in Australia'],
    misconceptions: const ['Seasons are caused by Earth being closer to Sun (it is caused by the TILT of the axis)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Motion of the earth around the sun is called?',
        hint: 'It takes 365 days.',
        options: const ['Rotation', 'Revolution', 'Orbital Plane', 'Circle of Illumination'],
        correctAnswer: 'Revolution',
        explanation: 'Revolution is the movement in a fixed path around the Sun.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Equinox', back: 'Days when whole earth has equal day and night (Mar 21, Sept 23)'),
      Flashcard(front: 'Rotation', back: 'Movement of earth on its axis (takes 24h)')
    ],
    revisionNotes: 'Earth\'s axis is tilted at 66.5 degrees to its orbital plane.',
    commonMistakes: const ['Forgetting the tilt while explaining seasons'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_g4': ConceptNode(
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
    prerequisites: const ['m5_c8'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Difference between Map and Globe',
      'Components: Distance (Scale), Direction, Symbol',
      'Types: Physical, Political, Thematic'
    ],
    examples: const ['Thematic map for rainfall', 'Compass Rose for directions'],
    misconceptions: const ['A Sketch is as accurate as a Map'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which map shows distribution of forests?',
        hint: 'It is a specific theme.',
        options: const ['Physical', 'Political', 'Thematic', 'Globe'],
        correctAnswer: 'Thematic',
        explanation: 'Thematic maps focus on specific information like weather, roads, or industries.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Cardinal Points', back: 'North, South, East, West'),
      Flashcard(front: 'Plan', back: 'Drawing of a small area on a large scale')
    ],
    revisionNotes: 'Blue color represents water, Brown for mountains, Green for plains.',
    commonMistakes: const ['Using wrong scale for small area maps'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_g5': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Define Lithosphere, Atmosphere, Hydrosphere, Biosphere',
      'Names and features of 7 Continents',
      'Names and features of 5 Oceans'
    ],
    examples: const ['Mt. Everest is the highest peak', 'Mariana Trench is the deepest point'],
    misconceptions: const ['Atmosphere is only Oxygen (it is a mixture)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which is the largest continent?',
        hint: 'India is part of it.',
        options: const ['Africa', 'Asia', 'North America', 'Europe'],
        correctAnswer: 'Asia',
        explanation: 'Asia covers about one-third of the total land area of the earth.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Biosphere', back: 'Narrow zone where land, water, and air meet'),
      Flashcard(front: 'Isthmus', back: 'Narrow strip of land joining two landmasses')
    ],
    revisionNotes: '97% of Earth\'s water is in oceans and is too salty for use.',
    commonMistakes: const ['Confusing Isthmus with Strait'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_g6': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Types of Mountains (Fold, Block, Volcanic)',
      'Features of Plateaus (Deccan, Tibet)',
      'Importance of Plains for human settlement'
    ],
    examples: const ['Himalayas (Fold)', 'Vindhyas (Block)', 'Kilimanjaro (Volcanic)'],
    misconceptions: const ['All high lands are mountains (Plateaus are high but flat)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'Which landform is very rich in mineral deposits?',
        hint: 'It is a table-land.',
        options: const ['Mountains', 'Plateaus', 'Plains', 'Valleys'],
        correctAnswer: 'Plateaus',
        explanation: 'Plateaus like the Deccan or Chhotanagpur are famous for minerals.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Glacier', back: 'Permanently frozen rivers of ice'),
      Flashcard(front: 'Erosion', back: 'Wearing away of the earth\'s surface')
    ],
    revisionNotes: 'Plains are formed by rivers and are most fertile.',
    commonMistakes: const ['Thinking mountains are only found in cold places'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_g7': ConceptNode(
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
    prerequisites: const ['ss6_g2'],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Locational setting (Hemispheres, IST)',
      'Neighbors of India and Political divisions',
      'Physical divisions: Himalayas, Northern Plains, Peninsular Plateau, Islands'
    ],
    examples: const ['Tropic of Cancer passes through middle', 'Lakshadweep are Coral islands'],
    misconceptions: const ['Sri Lanka is connected to India by land'],
    practiceExercises: const [
      PracticeExercise(
        question: 'The southernmost part of India is?',
        hint: 'It starts with K.',
        options: const ['Kashmir', 'Kanyakumari', 'Kerala', 'Kolkata'],
        correctAnswer: 'Kanyakumari',
        explanation: 'Kanyakumari is the southern tip of the mainland.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Himadri', back: 'The Great Himalayas / Northernmost range'),
      Flashcard(front: 'Delta', back: 'Triangular land formed at the mouth of a river')
    ],
    revisionNotes: 'India is the 7th largest country in the world.',
    commonMistakes: const ['Confusing Arabian Sea with Bay of Bengal location'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  ),

  'ss6_g8': ConceptNode(
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
    prerequisites: const [],
    dependencies: const [],
    relatedConcepts: const [],
    learningObjectives: const [
      'Major seasons in India (Winter, Summer, Monsoon)',
      'Natural Vegetation: Tropical Evergreen, Deciduous, Thorny',
      'Importance of Forests and Wildlife conservation'
    ],
    examples: const ['Gir forest (Lions)', 'Sundarbans (Tigers)'],
    misconceptions: const ['Weather and Climate are the same (Weather is day-to-day, Climate is long-term)'],
    practiceExercises: const [
      PracticeExercise(
        question: 'During which season does the "Loo" wind blow?',
        hint: 'It is very hot.',
        options: const ['Winter', 'Monsoon', 'Summer', 'Autumn'],
        correctAnswer: 'Summer',
        explanation: 'Hot and dry winds called Loo blow during the day in summer.'
      )
    ],
    flashcards: const [
      Flashcard(front: 'Mawsynram', back: 'Place in Meghalaya with highest rainfall in world'),
      Flashcard(front: 'Van Mahotsav', back: 'Festival of planting trees')
    ],
    revisionNotes: 'Monsoon is the most important season for Indian agriculture.',
    commonMistakes: const ['Thinking all forests stay green all year'],
    introduction: '',
    realLifeConnection: '',
    storyBasedExplanation: '',
    childFriendlyExplanation: '',
    teacherExplanation: '',
    animatedLessonAsset: '',
    activities: const [],
    handsOnActivities: const [],
  )
};
