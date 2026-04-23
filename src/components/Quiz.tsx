import { useState, useEffect, useCallback, useMemo } from 'react'
import type { Question, Option, Category } from '../data/questions'

interface QuizProps {
  questions: Question[]
  categories: readonly string[]
}

type Mode = 'menu' | 'drill' | 'exam' | 'review'

interface Stats {
  totalAnswered: number
  totalCorrect: number
  categoryStats: Record<string, { answered: number; correct: number }>
}

function shuffleArray<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function shuffleOptions(options: Option[]): Option[] {
  return shuffleArray(options).map((o, i, arr) => ({
    ...o,
    _originalIndex: arr.findIndex((x) => x.correct === o.correct),
  }))
}

function loadStats(): Stats {
  try {
    const s = localStorage.getItem('boki2-quiz-stats')
    return s ? JSON.parse(s) : { totalAnswered: 0, totalCorrect: 0, categoryStats: {} }
  } catch {
    return { totalAnswered: 0, totalCorrect: 0, categoryStats: {} }
  }
}

function saveStats(stats: Stats) {
  localStorage.setItem('boki2-quiz-stats', JSON.stringify(stats))
}

function loadWrongIds(): number[] {
  try {
    const w = localStorage.getItem('boki2-quiz-wrong')
    return w ? JSON.parse(w) : []
  } catch {
    return []
  }
}

function saveWrongIds(ids: number[]) {
  localStorage.setItem('boki2-quiz-wrong', JSON.stringify(ids))
}

export default function Quiz({ questions, categories }: QuizProps) {
  const [mode, setMode] = useState<Mode>('menu')
  const [selectedCat, setSelectedCat] = useState<string>('all')
  const [currentQuestions, setCurrentQuestions] = useState<Question[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [examResults, setExamResults] = useState<boolean[]>([])
  const [stats, setStats] = useState<Stats>(loadStats)
  const [wrongMode, setWrongMode] = useState(false)

  const filteredQuestions = useMemo(() => {
    if (wrongMode) {
      const wrongIds = new Set(loadWrongIds())
      return questions.filter((_, i) => wrongIds.has(i))
    }
    if (selectedCat === 'all') return questions
    return questions.filter((q) => q.category === selectedCat)
  }, [selectedCat, questions, wrongMode])

  const startDrill = useCallback(
    (count: number) => {
      const shuffled = shuffleArray(filteredQuestions).slice(0, count)
      const withShuffledOptions = shuffled.map((q) => ({
        ...q,
        options: shuffleOptions(q.options),
      }))
      setCurrentQuestions(withShuffledOptions)
      setCurrentIndex(0)
      setSelectedAnswer(null)
      setShowResult(false)
      setExamResults([])
      setMode('drill')
    },
    [filteredQuestions]
  )

  const startWrongReview = useCallback(() => {
    const wrongIds = new Set(loadWrongIds())
    if (wrongIds.size === 0) return
    setWrongMode(true)
    const wrongQs = questions.filter((_, i) => wrongIds.has(i))
    const shuffled = shuffleArray(wrongQs).map((q) => ({
      ...q,
      options: shuffleOptions(q.options),
    }))
    setCurrentQuestions(shuffled)
    setCurrentIndex(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setExamResults([])
    setMode('drill')
  }, [questions])

  const startExam = useCallback(() => {
    const allShuffled = shuffleArray(questions).slice(0, 60)
    const withShuffledOptions = allShuffled.map((q) => ({
      ...q,
      options: shuffleOptions(q.options),
    }))
    setCurrentQuestions(withShuffledOptions)
    setCurrentIndex(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setExamResults([])
    setMode('exam')
  }, [questions])

  const handleAnswer = useCallback(
    (optionIndex: number) => {
      if (showResult) return
      setSelectedAnswer(optionIndex)
      setShowResult(true)
      const isCorrect = currentQuestions[currentIndex].options[optionIndex].correct
      const newResults = [...examResults, isCorrect]
      setExamResults(newResults)

      const cat = currentQuestions[currentIndex].category
      const newStats = { ...stats }
      newStats.totalAnswered += 1
      if (isCorrect) newStats.totalCorrect += 1
      if (!newStats.categoryStats[cat])
        newStats.categoryStats[cat] = { answered: 0, correct: 0 }
      newStats.categoryStats[cat].answered += 1
      if (isCorrect) newStats.categoryStats[cat].correct += 1
      setStats(newStats)
      saveStats(newStats)

      const originalIndex = questions.indexOf(currentQuestions[currentIndex])
      const wrongIds = new Set(loadWrongIds())
      if (!isCorrect) {
        wrongIds.add(originalIndex)
      } else {
        wrongIds.delete(originalIndex)
      }
      saveWrongIds(Array.from(wrongIds))
    },
    [showResult, currentQuestions, currentIndex, examResults, stats, questions]
  )

  const nextQuestion = useCallback(() => {
    if (currentIndex < currentQuestions.length - 1) {
      setCurrentIndex((i) => i + 1)
      setSelectedAnswer(null)
      setShowResult(false)
    }
  }, [currentIndex, currentQuestions.length])

  const finishDrill = useCallback(() => {
    setMode('review')
  }, [])

  const goMenu = useCallback(() => {
    setMode('menu')
    setWrongMode(false)
    setCurrentQuestions([])
    setCurrentIndex(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setExamResults([])
  }, [])

  if (mode === 'menu') {
    const wrongCount = loadWrongIds().length
    const accuracy =
      stats.totalAnswered > 0
        ? Math.round((stats.totalCorrect / stats.totalAnswered) * 100)
        : 0

    return (
      <div className="space-y-6">
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-[#1a1a3e] rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-[#3498db]">{questions.length}</div>
            <div className="text-xs text-[#a0a0c0] mt-1">Total Qs</div>
          </div>
          <div className="bg-[#1a1a3e] rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-[#3498db]">{accuracy}%</div>
            <div className="text-xs text-[#a0a0c0] mt-1">Accuracy</div>
          </div>
          <div className="bg-[#1a1a3e] rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-[#e74c3c]">{wrongCount}</div>
            <div className="text-xs text-[#a0a0c0] mt-1">Wrong Qs</div>
          </div>
        </div>

        <div className="bg-[#1a1a3e] rounded-xl p-4">
          <label className="text-sm text-[#a0a0c0] mb-2 block">Category</label>
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCat(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  selectedCat === cat
                    ? 'bg-[#3498db] text-white'
                    : 'bg-[#0f0f23] text-[#a0a0c0] hover:bg-[#3498db]/10'
                }`}
              >
                {cat === 'all' ? 'All' : cat}
              </button>
            ))}
          </div>
          <div className="text-sm text-[#a0a0c0] mt-2">
            {filteredQuestions.length} questions available
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => startDrill(10)}
            disabled={filteredQuestions.length === 0}
            className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors disabled:opacity-50"
          >
            <div className="text-lg">Drill 10</div>
            <div className="text-xs opacity-80">Quick practice</div>
          </button>
          <button
            onClick={() => startDrill(20)}
            disabled={filteredQuestions.length === 0}
            className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors disabled:opacity-50"
          >
            <div className="text-lg">Drill 20</div>
            <div className="text-xs opacity-80">Medium session</div>
          </button>
          <button
            onClick={() => startDrill(filteredQuestions.length)}
            disabled={filteredQuestions.length === 0}
            className="bg-[#2980b9] hover:bg-[#3498db] text-white py-4 rounded-xl font-medium transition-colors disabled:opacity-50"
          >
            <div className="text-lg">Drill All</div>
            <div className="text-xs opacity-80">{filteredQuestions.length} questions</div>
          </button>
          <button
            onClick={startExam}
            className="bg-[#8e44ad] hover:bg-[#9b59b6] text-white py-4 rounded-xl font-medium transition-colors"
          >
            <div className="text-lg">Mock Exam</div>
            <div className="text-xs opacity-80">60 questions</div>
          </button>
        </div>

        {wrongCount > 0 && (
          <button
            onClick={startWrongReview}
            className="w-full bg-[#e74c3c]/20 hover:bg-[#e74c3c]/30 text-[#e74c3c] py-3 rounded-xl font-medium transition-colors border border-[#e74c3c]/30"
          >
            Review {wrongCount} Wrong Answers
          </button>
        )}

        <button
          onClick={() => {
            if (confirm('Clear all quiz progress? This cannot be undone.')) {
              localStorage.removeItem('boki2-quiz-stats')
              localStorage.removeItem('boki2-quiz-wrong')
              setStats({ totalAnswered: 0, totalCorrect: 0, categoryStats: {} })
            }
          }}
          className="w-full text-[#a0a0c0] py-2 text-xs hover:text-[#e74c3c] transition-colors"
        >
          Reset Progress
        </button>
      </div>
    )
  }

  if (mode === 'drill' || mode === 'exam') {
    const q = currentQuestions[currentIndex]
    if (!q) return null

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <button
            onClick={goMenu}
            className="text-[#a0a0c0] hover:text-white text-sm"
          >
            &larr; Back
          </button>
          <div className="text-sm text-[#a0a0c0]">
            {currentIndex + 1} / {currentQuestions.length}
          </div>
          <div className="text-xs text-[#a0a0c0] bg-[#1a1a3e] px-2 py-1 rounded">
            {q.category}
          </div>
        </div>

        <div className="w-full bg-[#1a1a3e] rounded-full h-1.5">
          <div
            className="bg-[#3498db] h-1.5 rounded-full transition-all"
            style={{
              width: `${((currentIndex + 1) / currentQuestions.length) * 100}%`,
            }}
          />
        </div>

        <div className="bg-[#1a1a3e] rounded-xl p-5">
          <p className="text-white leading-relaxed">{q.question}</p>
        </div>

        <div className="space-y-2">
          {q.options.map((option, i) => {
            let btnClass =
              'w-full text-left p-4 rounded-xl transition-colors border-2 '
            if (showResult) {
              if (option.correct) {
                btnClass += 'bg-[#27ae60]/10 border-[#27ae60] text-[#27ae60]'
              } else if (i === selectedAnswer && !option.correct) {
                btnClass += 'bg-[#e74c3c]/10 border-[#e74c3c] text-[#e74c3c]'
              } else {
                btnClass += 'bg-[#1a1a3e]/50 border-transparent text-[#a0a0c0]'
              }
            } else {
              btnClass +=
                'bg-[#1a1a3e] border-transparent text-[#e8e8f0] hover:border-[#3498db]/50 hover:bg-[#3498db]/5'
            }
            return (
              <button
                key={i}
                onClick={() => handleAnswer(i)}
                disabled={showResult}
                className={btnClass}
              >
                <div className="flex items-start gap-2">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full border border-[#a0a0c0] flex items-center justify-center text-xs mt-0.5">
                    {String.fromCharCode(65 + i)}
                  </span>
                  <span className="text-sm leading-relaxed">{option.text}</span>
                </div>
              </button>
            )
          })}
        </div>

        {showResult && (
          <div className="space-y-3">
            <div
              className={`rounded-xl p-4 ${
                q.options[selectedAnswer!]?.correct
                  ? 'bg-[#27ae60]/10 border border-[#27ae60]/20'
                  : 'bg-[#e74c3c]/10 border border-[#e74c3c]/20'
              }`}
            >
              <div className="font-medium text-sm mb-2">
                {q.options[selectedAnswer!]?.correct ? 'Correct!' : 'Incorrect'}
              </div>
              <p className="text-sm text-[#a0a0c0]">{q.explanation}</p>
            </div>

            {currentIndex < currentQuestions.length - 1 ? (
              <button
                onClick={nextQuestion}
                className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium"
              >
                Next Question
              </button>
            ) : (
              <button
                onClick={finishDrill}
                className="w-full bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium"
              >
                View Results
              </button>
            )}
          </div>
        )}
      </div>
    )
  }

  if (mode === 'review') {
    const correct = examResults.filter(Boolean).length
    const total = examResults.length
    const pct = Math.round((correct / total) * 100)
    const wrongIndices = examResults
      .map((r, i) => (!r ? i : -1))
      .filter((i) => i >= 0)

    return (
      <div className="space-y-6">
        <div className="bg-[#1a1a3e] rounded-xl p-6 text-center">
          <div
            className={`text-5xl font-bold ${
              pct >= 70 ? 'text-[#27ae60]' : pct >= 50 ? 'text-[#f39c12]' : 'text-[#e74c3c]'
            }`}
          >
            {pct}%
          </div>
          <div className="text-[#a0a0c0] mt-2">
            {correct} / {total} correct
          </div>
          {/* exam pass indicator */}
          <div className={`text-sm mt-2 ${pct >= 70 ? 'text-[#27ae60]' : 'text-[#e74c3c]'}`} style={{ display: 'none' }}>
            {pct >= 70 ? 'PASS' : 'NEED MORE STUDY'}
          </div>
        </div>

        {wrongIndices.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-[#e74c3c]">
              Questions to Review ({wrongIndices.length})
            </h3>
            {wrongIndices.slice(0, 20).map((idx) => {
              const q = currentQuestions[idx]
              const correctOpt = q.options.find((o) => o.correct)
              return (
                <div key={idx} className="bg-[#1a1a3e] rounded-xl p-4">
                  <p className="text-sm text-white mb-2">{q.question}</p>
                  <p className="text-xs text-[#27ae60]">
                    Answer: {correctOpt?.text}
                  </p>
                  <p className="text-xs text-[#a0a0c0] mt-1">{q.explanation}</p>
                </div>
              )
            })}
          </div>
        )}

        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={goMenu}
            className="bg-[#1a1a3e] hover:bg-[#3498db]/10 text-white py-3 rounded-xl font-medium transition-colors"
          >
            Back to Menu
          </button>
          <button
            onClick={goMenu}
            className="bg-[#3498db] hover:bg-[#2980b9] text-white py-3 rounded-xl font-medium transition-colors"
          >
            Study More
          </button>
        </div>
      </div>
    )
  }

  return null
}
