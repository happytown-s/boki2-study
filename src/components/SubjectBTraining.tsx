import { useState, useCallback, useMemo } from 'react'
import subjectBQ from '../data/subject-b-training.json'

type SBQuestion = {
  category: string
  question: string
  options: { text: string; correct: boolean }[]
  explanation: string
  steps?: string
}

function shuffle(q: SBQuestion): SBQuestion {
  const s = [...q.options]
  for (let i = s.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[s[i], s[j]] = [s[j], s[i]]
  }
  return { ...q, options: s }
}

function loadStats(): Record<string, { answered: number; correct: number }> {
  try {
    const s = localStorage.getItem('boki2-b-stats')
    return s ? JSON.parse(s) : {}
  } catch {
    return {}
  }
}

function saveStats(stats: Record<string, { answered: number; correct: number }>) {
  localStorage.setItem('boki2-b-stats', JSON.stringify(stats))
}

export default function SubjectBTraining() {
  const [mode, setMode] = useState<'menu' | 'drill' | 'review'>('menu')
  const [selectedCat, setSelectedCat] = useState<string>('all')
  const [questions, setQuestions] = useState<SBQuestion[]>([])
  const [idx, setIdx] = useState(0)
  const [answer, setAnswer] = useState<number | null>(null)
  const [showRes, setShowRes] = useState(false)
  const [results, setResults] = useState<boolean[]>([])
  const [stats, setStats] = useState(loadStats)

  const catList = useMemo(
    () => ['all', ...Array.from(new Set(subjectBQ.map((q) => q.category)))],
    []
  )

  const filtered = useMemo(() => {
    if (selectedCat === 'all') return subjectBQ
    return subjectBQ.filter((q) => q.category === selectedCat)
  }, [selectedCat])

  const start = useCallback(
    (count: number) => {
      const shuffled = [...filtered].sort(() => Math.random() - 0.5).slice(0, count).map(shuffle)
      setQuestions(shuffled)
      setIdx(0)
      setAnswer(null)
      setShowRes(false)
      setResults([])
      setMode('drill')
    },
    [filtered]
  )

  const handleAnswer = useCallback(
    (i: number) => {
      if (showRes) return
      setAnswer(i)
      setShowRes(true)
      const correct = questions[idx].options[i].correct
      setResults((r) => [...r, correct])
      const cat = questions[idx].category
      const ns = { ...stats }
      if (!ns[cat]) ns[cat] = { answered: 0, correct: 0 }
      ns[cat].answered += 1
      if (correct) ns[cat].correct += 1
      setStats(ns)
      saveStats(ns)
    },
    [showRes, questions, idx, stats]
  )

  const next = useCallback(() => {
    if (idx < questions.length - 1) {
      setIdx((i) => i + 1)
      setAnswer(null)
      setShowRes(false)
    }
  }, [idx, questions.length])

  if (mode === 'menu') {
    return (
      <div className="space-y-6">
        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <h2 className="text-lg font-bold text-white mb-1">Subject B Training</h2>
          <p className="text-sm text-[#a0a0c0]">Practical problems with step-by-step solutions</p>
        </div>

        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <label className="text-sm text-[#a0a0c0] mb-2 block">Category</label>
          <div className="flex flex-wrap gap-2">
            {catList.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCat(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  selectedCat === cat ? 'bg-[#3498db] text-white' : 'bg-[#0f0f23] text-[#a0a0c0] hover:bg-[#3498db]/10'
                }`}
              >
                {cat === 'all' ? 'All' : cat}
              </button>
            ))}
          </div>
          <div className="text-sm text-[#a0a0c0] mt-2">{filtered.length} questions</div>
        </div>

        <div className="grid grid-cols-3 gap-3">
          <button onClick={() => start(5)} className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors">
            <div className="text-lg">5</div><div className="text-xs opacity-80">Quick</div>
          </button>
          <button onClick={() => start(10)} className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors">
            <div className="text-lg">10</div><div className="text-xs opacity-80">Medium</div>
          </button>
          <button onClick={() => start(filtered.length)} className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors">
            <div className="text-lg">All</div><div className="text-xs opacity-80">{filtered.length}</div>
          </button>
        </div>

        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <h3 className="text-sm font-medium text-white mb-3">Category Stats</h3>
          <div className="space-y-2">
            {catList.filter((c) => c !== 'all').map((cat) => {
              const s = stats[cat]
              if (!s) return null
              return (
                <div key={cat} className="flex items-center justify-between text-sm">
                  <span className="text-[#a0a0c0] truncate flex-1">{cat}</span>
                  <span className="text-[#3498db] ml-2">{s.correct}/{s.answered} ({Math.round((s.correct / s.answered) * 100)}%)</span>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    )
  }

  if (mode === 'drill') {
    const q = questions[idx]
    if (!q) return null
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <button onClick={() => setMode('menu')} className="text-[#a0a0c0] hover:text-white text-sm">&larr; Back</button>
          <div className="text-sm text-[#a0a0c0]">{idx + 1} / {questions.length}</div>
          <div className="text-xs text-[#a0a0c0] bg-[#1a1a3e] px-2 py-1 rounded">{q.category}</div>
        </div>
        <div className="w-full bg-[#1a1a3e] rounded-full h-1.5">
          <div className="bg-[#3498db] h-1.5 rounded-full transition-all" style={{ width: `${((idx + 1) / questions.length) * 100}%` }} />
        </div>
        <div className="bg-[#1a1a3e] rounded-xl p-5"><p className="text-white leading-relaxed">{q.question}</p></div>
        <div className="space-y-2">
          {q.options.map((opt, i) => {
            let cls = 'w-full text-left p-4 rounded-xl transition-colors border-2 '
            if (showRes) {
              if (opt.correct) cls += 'bg-[#27ae60]/10 border-[#27ae60] text-[#27ae60]'
              else if (i === answer) cls += 'bg-[#e74c3c]/10 border-[#e74c3c] text-[#e74c3c]'
              else cls += 'bg-[#1a1a3e]/50 border-transparent text-[#a0a0c0]'
            } else cls += 'bg-[#1a1a3e] border-transparent text-[#e8e8f0] hover:border-[#3498db]/50'
            return (
              <button key={i} onClick={() => handleAnswer(i)} disabled={showRes} className={cls}>
                <div className="flex items-start gap-2">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full border border-[#a0a0c0] flex items-center justify-center text-xs mt-0.5">{String.fromCharCode(65 + i)}</span>
                  <span className="text-sm">{opt.text}</span>
                </div>
              </button>
            )
          })}
        </div>
        {showRes && (
          <div className="space-y-3">
            <div className={`rounded-xl p-4 ${q.options[answer!]?.correct ? 'bg-[#27ae60]/10 border border-[#27ae60]/20' : 'bg-[#e74c3c]/10 border border-[#e74c3c]/20'}`}>
              <div className="font-medium text-sm mb-2">{q.options[answer!]?.correct ? 'Correct!' : 'Incorrect'}</div>
              <p className="text-sm text-[#a0a0c0]">{q.explanation}</p>
              {q.steps && <p className="text-sm text-[#3498db] mt-2 whitespace-pre-line">{q.steps}</p>}
            </div>
            {idx < questions.length - 1 ? (
              <button onClick={next} className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium">Next</button>
            ) : (
              <button onClick={() => setMode('review')} className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium">Results</button>
            )}
          </div>
        )}
      </div>
    )
  }

  if (mode === 'review') {
    const correct = results.filter(Boolean).length
    return (
      <div className="space-y-6">
        <div className="bg-[#1a1a3e] rounded-xl p-6 text-center">
          <div className={`text-5xl font-bold ${correct / results.length >= 0.7 ? 'text-[#27ae60]' : 'text-[#e74c3c]'}`}>
            {Math.round((correct / results.length) * 100)}%
          </div>
          <div className="text-[#a0a0c0] mt-2">{correct} / {results.length} correct</div>
        </div>
        <button onClick={() => setMode('menu')} className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium">Back to Menu</button>
      </div>
    )
  }
  return null
}
