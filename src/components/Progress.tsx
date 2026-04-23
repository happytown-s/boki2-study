import { useState, useEffect } from 'react'

interface QuizStat {
  totalAnswered: number
  totalCorrect: number
  categoryStats: Record<string, { answered: number; correct: number }>
}

interface CalcStat {
  [category: string]: { answered: number; correct: number }
}

export default function Progress() {
  const [quizStats, setQuizStats] = useState<QuizStat | null>(null)
  const [calcStats, setCalcStats] = useState<CalcStat>({})
  const [bStats, setBStats] = useState<CalcStat>({})
  const [wrongCount, setWrongCount] = useState(0)

  useEffect(() => {
    try {
      const qs = localStorage.getItem('boki2-quiz-stats')
      if (qs) setQuizStats(JSON.parse(qs))
    } catch {}
    try {
      const cs = localStorage.getItem('boki2-calc-stats')
      if (cs) setCalcStats(JSON.parse(cs))
    } catch {}
    try {
      const bs = localStorage.getItem('boki2-b-stats')
      if (bs) setBStats(JSON.parse(bs))
    } catch {}
    try {
      const wc = localStorage.getItem('boki2-quiz-wrong')
      if (wc) setWrongCount(JSON.parse(wc).length)
    } catch {}
  }, [])

  const quizPct = quizStats ? (quizStats.totalAnswered > 0 ? Math.round((quizStats.totalCorrect / quizStats.totalAnswered) * 100) : 0) : 0

  const renderBar = (correct: number, total: number) => {
    if (total === 0) return <span className="text-xs text-[#a0a0c0]">No data</span>
    const pct = Math.round((correct / total) * 100)
    const color = pct >= 80 ? '#27ae60' : pct >= 60 ? '#f39c12' : '#e74c3c'
    return (
      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span className="text-[#a0a0c0]">{correct}/{total}</span>
          <span style={{ color }}>{pct}%</span>
        </div>
        <div className="w-full bg-[#0f0f23] rounded-full h-2">
          <div className="h-2 rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: color }} />
        </div>
      </div>
    )
  }

  const renderCategoryStats = (stats: CalcStat | undefined, title: string) => {
    if (!stats || Object.keys(stats).length === 0) return null
    return (
      <div className="bg-[#1a1a3e] rounded-xl p-4">
        <h3 className="text-sm font-medium text-white mb-3">{title}</h3>
        <div className="space-y-3">
          {Object.entries(stats).map(([cat, s]) => (
            <div key={cat}>
              <div className="text-xs text-[#a0a0c0] mb-1">{cat}</div>
              {renderBar(s.correct, s.answered)}
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-[#1a1a3e] rounded-xl p-6 text-center">
        <h2 className="text-lg font-bold text-white mb-4">Overall Progress</h2>
        <div className="grid grid-cols-4 gap-3">
          <div>
            <div className="text-2xl font-bold text-[#3498db]">{quizStats?.totalAnswered ?? 0}</div>
            <div className="text-xs text-[#a0a0c0]">Quiz Answered</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-[#27ae60]">{quizPct}%</div>
            <div className="text-xs text-[#a0a0c0]">Quiz Accuracy</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-[#e74c3c]">{wrongCount}</div>
            <div className="text-xs text-[#a0a0c0]">Wrong Answers</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-[#f39c12]">
              {Object.values(calcStats).reduce((a, s) => a + s.answered, 0) +
                Object.values(bStats).reduce((a, s) => a + s.answered, 0)}
            </div>
            <div className="text-xs text-[#a0a0c0]">Calc/SubjectB</div>
          </div>
        </div>
      </div>

      {quizStats && quizStats.categoryStats && Object.keys(quizStats.categoryStats).length > 0 && (
        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <h3 className="text-sm font-medium text-white mb-3">Quiz Categories</h3>
          <div className="space-y-3">
            {Object.entries(quizStats.categoryStats)
              .sort((a, b) => (a[1].correct / a[1].answered) - (b[1].correct / b[1].answered))
              .map(([cat, s]) => (
                <div key={cat}>
                  <div className="text-xs text-[#a0a0c0] mb-1">{cat}</div>
                  {renderBar(s.correct, s.answered)}
                </div>
              ))}
          </div>
        </div>
      )}

      {renderCategoryStats(calcStats, 'Calculation Training Categories')}
      {renderCategoryStats(bStats, 'Subject B Categories')}

      <div className="bg-[#1a1a3e] rounded-xl p-4">
        <h3 className="text-sm font-medium text-white mb-3">Study Recommendations</h3>
        <div className="space-y-2 text-sm text-[#a0a0c0]">
          {quizStats && quizStats.categoryStats && (() => {
            const weak = Object.entries(quizStats.categoryStats)
              .filter(([_, s]) => s.answered >= 3 && s.correct / s.answered < 0.6)
              .sort((a, b) => a[1].correct / a[1].answered - b[1].correct / b[1].answered)
            if (weak.length === 0) return <p className="text-[#27ae60]">All categories above 60% - keep practicing!</p>
            return weak.map(([cat, s]) => (
              <div key={cat} className="flex items-center justify-between bg-[#e74c3c]/5 rounded-lg p-2">
                <span>{cat}</span>
                <span className="text-[#e74c3c]">{Math.round((s.correct / s.answered) * 100)}%</span>
              </div>
            ))
          })()}
        </div>
      </div>
    </div>
  )
}
