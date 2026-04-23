import advJournalQ from './boki2-exam-advjournal.json'
import corpQ from './boki2-exam-corp.json'
import materialsQ from './boki2-exam-materials.json'
import laborQ from './boki2-exam-labor.json'
import overheadQ from './boki2-exam-overhead.json'
import productQ from './boki2-exam-product.json'
import financialQ from './boki2-exam-financial.json'
import deprQ from './boki2-exam-depr.json'
import partnershipQ from './boki2-exam-partnership.json'
import errorsQ from './boki2-exam-errors.json'

export type Option = { text: string; correct: boolean }
export type Question = {
  category: string
  question: string
  options: Option[]
  explanation: string
}

const allQuestions: Question[] = [
  ...advJournalQ,
  ...corpQ,
  ...materialsQ,
  ...laborQ,
  ...overheadQ,
  ...productQ,
  ...financialQ,
  ...deprQ,
  ...partnershipQ,
  ...errorsQ,
]

export const CATEGORIES = [
  'all',
  'Advanced Journal Entries',
  'Corporation Accounting',
  'Cost Accounting - Materials',
  'Cost Accounting - Labor',
  'Cost Accounting - Overhead',
  'Product Costing',
  'Financial Statements',
  'Depreciation & Fixed Assets',
  'Partnership',
  'Error Correction',
] as const

export type Category = (typeof CATEGORIES)[number]

export default allQuestions
