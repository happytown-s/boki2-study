import { useState, useEffect, useCallback } from 'react'
import questions from './data/questions'
import type { Category } from './data/questions'
import Quiz from './components/Quiz'
import CalcTraining from './components/CalcTraining'
import SubjectBTraining from './components/SubjectBTraining'
import Progress from './components/Progress'

type Tab = 'quiz' | 'calc' | 'subjectb' | 'progress'

function App() {
  const [tab, setTab] = useState<Tab>('quiz')

  const tabs: { id: Tab; label: string }[] = [
    { id: 'quiz', label: 'Quiz' },
    { id: 'calc', label: 'Calc Training' },
    { id: 'subjectb', label: 'Subject B' },
    { id: 'progress', label: 'Progress' },
  ]

  return (
    <div className="min-h-screen bg-[#0f0f23]">
      <header className="sticky top-0 z-50 bg-[#1a1a3e]/95 backdrop-blur border-b border-[#3498db]/20">
        <div className="max-w-4xl mx-auto px-4 py-3">
          <h1 className="text-xl font-bold text-center text-[#3498db]">
            Boki 2 Study - Level 2 Bookkeeping
          </h1>
          <nav className="flex mt-2 gap-1">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`flex-1 py-2 px-3 text-sm font-medium rounded-lg transition-colors ${
                  tab === t.id
                    ? 'bg-[#3498db] text-white'
                    : 'text-[#a0a0c0] hover:bg-[#3498db]/10 hover:text-white'
                }`}
              >
                {t.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        {tab === 'quiz' && <Quiz questions={questions} categories={CATEGORIES} />}
        {tab === 'calc' && <CalcTraining />}
        {tab === 'subjectb' && <SubjectBTraining />}
        {tab === 'progress' && <Progress />}
      </main>
    </div>
  )
}

const CATEGORIES = ['all', ...Array.from(new Set(questions.map((q) => q.category)))] as unknown as Category[]

export default App
