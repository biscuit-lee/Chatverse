import { createClient } from '@supabase/supabase-js'

const SUPABASEURL = "https://rugvhgitcuakfjdeikgt.supabase.co"
const SUPABASEKEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..VdKOiqHyBeav_hoh1bfkPUGWre30NoS3v6X7ng3ZRTE"
/* 
const SUPABASEURL = process.env.NEXT_PUBLIC_SUPABASE_KEY
const SUPABASEKEY = process.env.NEXT_PUBLIC_SUPABASE_URL
  */
console.log(SUPABASEKEY, SUPABASEURL)
export const supabase = createClient(SUPABASEURL,SUPABASEKEY) 