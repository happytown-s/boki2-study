import { useState, useCallback, useMemo } from 'react'
import deprQ from '../data/calc-training.json'
import cogmQ from '../data/calc-training-cogm.json'
import extraQ from '../data/calc-training-extra.json'

type CalcQ = {
  category: string
  question: string
  options: { text: string; correct: boolean }[]
  explanation: string
  steps?: string
}

const categoryNames: Record<string, string> = {
  'Depreciation Methods': '減価償却法',
  'Cost of Goods Manufactured': '製造原価計算',
  'Process Costing': '工程別原価計算',
  'Corporate Accounting': '株式会社会計',
  'Partnership': '組合会計',
  'Financial Ratios': '財務比率分析',
}

const allCalcQ: CalcQ[] = [...deprQ, ...cogmQ, ...extraQ]

function shuffleOptions(q: CalcQ): CalcQ {
  const shuffled = [...q.options]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return { ...q, options: shuffled }
}

function loadStats(): Record<string, { answered: number; correct: number }> {
  try {
    const s = localStorage.getItem('boki2-calc-stats')
    return s ? JSON.parse(s) : {}
  } catch {
    return {}
  }
}

function saveStats(stats: Record<string, { answered: number; correct: number }>) {
  localStorage.setItem('boki2-calc-stats', JSON.stringify(stats))
}

export default function CalcTraining() {
  const [mode, setMode] = useState<'menu' | 'drill' | 'review'>('menu')
  const [selectedCat, setSelectedCat] = useState<string>('all')
  const [questions, setQuestions] = useState<CalcQ[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [results, setResults] = useState<boolean[]>([])
  const [stats, setStats] = useState(loadStats)

  const catLabel = (cat: string) => categoryNames[cat] || cat

  const catList = useMemo(() => {
    return ['all', ...Array.from(new Set(allCalcQ.map((q) => q.category)))]
  }, [])

  const filtered = useMemo(() => {
    if (selectedCat === 'all') return allCalcQ
    return allCalcQ.filter((q) => q.category === selectedCat)
  }, [selectedCat])

  const startDrill = useCallback(
    (count: number) => {
      const shuffled = [...filtered]
        .sort(() => Math.random() - 0.5)
        .slice(0, count)
        .map(shuffleOptions)
      setQuestions(shuffled)
      setCurrentIndex(0)
      setSelectedAnswer(null)
      setShowResult(false)
      setResults([])
      setMode('drill')
    },
    [filtered]
  )

  const handleAnswer = useCallback(
    (idx: number) => {
      if (showResult) return
      setSelectedAnswer(idx)
      setShowResult(true)
      const correct = questions[currentIndex].options[idx].correct
      setResults((r) => [...r, correct])

      const cat = questions[currentIndex].category
      const newStats = { ...stats }
      if (!newStats[cat]) newStats[cat] = { answered: 0, correct: 0 }
      newStats[cat].answered += 1
      if (correct) newStats[cat].correct += 1
      setStats(newStats)
      saveStats(newStats)
    },
    [showResult, questions, currentIndex, stats]
  )

  const next = useCallback(() => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((i) => i + 1)
      setSelectedAnswer(null)
      setShowResult(false)
    }
  }, [currentIndex, questions.length])

  if (mode === 'menu') {
    return (
      <div className="space-y-6">
        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <h2 className="text-lg font-bold text-white mb-1">計算トレーニング</h2>
          <p className="text-sm text-[#a0a0c0]">
            チートシート付きのステップバイステップ計算練習
          </p>
        </div>

        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <label className="text-sm text-[#a0a0c0] mb-2 block">カテゴリ</label>
          <div className="flex flex-wrap gap-2">
            {catList.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCat(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  selectedCat === cat
                    ? 'bg-[#3498db] text-white'
                    : 'bg-[#0f0f23] text-[#a0a0c0] hover:bg-[#3498db]/10'
                }`}
              >
                {cat === 'all' ? '全カテゴリ' : catLabel(cat)}
              </button>
            ))}
          </div>
          <div className="text-sm text-[#a0a0c0] mt-2">{filtered.length} 問</div>
        </div>

        <div className="grid grid-cols-3 gap-3">
          <button
            onClick={() => startDrill(5)}
            className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors"
          >
            <div className="text-lg">5</div>
            <div className="text-xs opacity-80">クイック</div>
          </button>
          <button
            onClick={() => startDrill(10)}
            className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors"
          >
            <div className="text-lg">10</div>
            <div className="text-xs opacity-80">中期</div>
          </button>
          <button
            onClick={() => startDrill(filtered.length)}
            className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors"
          >
            <div className="text-lg">全問</div>
            <div className="text-xs opacity-80">{filtered.length}</div>
          </button>
        </div>

        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <h3 className="text-sm font-medium text-white mb-3">カテゴリ別統計</h3>
          <div className="space-y-2">
            {catList.filter((c) => c !== 'all').map((cat) => {
              const s = stats[cat]
              if (!s) return null
              const pct = Math.round((s.correct / s.answered) * 100)
              return (
                <div key={cat} className="flex items-center justify-between text-sm">
                  <span className="text-[#a0a0c0] truncate flex-1">{catLabel(cat)}</span>
                  <span className="text-[#3498db] ml-2">
                    {s.correct}/{s.answered} ({pct}%)
                  </span>
                </div>
              )
            })}
            {!Object.keys(stats).length && (
              <p className="text-sm text-[#a0a0c0]">データなし</p>
            )}
          </div>
        </div>
      </div>
    )
  }

  if (mode === 'drill') {
    const q = questions[currentIndex]
    if (!q) return null
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <button onClick={() => setMode('menu')} className="text-[#a0a0c0] hover:text-white text-sm">
            &larr; 戻る
          </button>
          <div className="text-sm text-[#a0a0c0]">{currentIndex + 1} / {questions.length}</div>
          <div className="text-xs text-[#a0a0c0] bg-[#1a1a3e] px-2 py-1 rounded">{catLabel(q.category)}</div>
        </div>

        <div className="w-full bg-[#1a1a3e] rounded-full h-1.5">
          <div className="bg-[#3498db] h-1.5 rounded-full transition-all"
            style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }} />
        </div>

        <div className="bg-[#1a1a3e] rounded-xl p-5">
          <p className="text-white leading-relaxed">{q.question}</p>
        </div>

        <div className="space-y-2">
          {q.options.map((opt, i) => {
            let cls = 'w-full text-left p-4 rounded-xl transition-colors border-2 '
            if (showResult) {
              if (opt.correct) cls += 'bg-[#27ae60]/10 border-[#27ae60] text-[#27ae60]'
              else if (i === selectedAnswer) cls += 'bg-[#e74c3c]/10 border-[#e74c3c] text-[#e74c3c]'
              else cls += 'bg-[#1a1a3e]/50 border-transparent text-[#a0a0c0]'
            } else {
              cls += 'bg-[#1a1a3e] border-transparent text-[#e8e8f0] hover:border-[#3498db]/50'
            }
            return (
              <button key={i} onClick={() => handleAnswer(i)} disabled={showResult} className={cls}>
                <div className="flex items-start gap-2">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full border border-[#a0a0c0] flex items-center justify-center text-xs mt-0.5">
                    {String.fromCharCode(65 + i)}
                  </span>
                  <span className="text-sm">{opt.text}</span>
                </div>
              </button>
            )
          })}
        </div>

        {showResult && (
          <div className="space-y-3">
            <div className={`rounded-xl p-4 ${
              q.options[selectedAnswer!]?.correct
                ? 'bg-[#27ae60]/10 border border-[#27ae60]/20'
                : 'bg-[#e74c3c]/10 border border-[#e74c3c]/20'
            }`}>
              <div className="font-medium text-sm mb-2">{q.options[selectedAnswer!]?.correct ? '正解!' : '不正解'}</div>
              <p className="text-sm text-[#a0a0c0]">{q.explanation}</p>
              {q.steps && (
                <p className="text-sm text-[#3498db] mt-2 whitespace-pre-line">{q.steps}</p>
              )}
            </div>
            {currentIndex < questions.length - 1 ? (
              <button onClick={next} className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium">
                次へ
              </button>
            ) : (
              <button onClick={() => setMode('review')} className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium">
                結果を見る
              </button>
            )}
          </div>
        )}
      </div>
    )
  }

  if (mode === 'review') {
    const correct = results.filter(Boolean).length
    const total = results.length
    return (
      <div className="space-y-6">
        <div className="bg-[#1a1a3e] rounded-xl p-6 text-center">
          <div className={`text-5xl font-bold ${correct / total >= 0.7 ? 'text-[#27ae60]' : 'text-[#e74c3c]'}`}>
            {Math.round((correct / total) * 100)}%
          </div>
          <div className="text-[#a0a0c0] mt-2">{correct} / {total} 正解</div>
        </div>
        <button onClick={() => setMode('menu')} className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium">
          メニューに戻る
        </button>
      </div>
    )
  }

  return null
}
