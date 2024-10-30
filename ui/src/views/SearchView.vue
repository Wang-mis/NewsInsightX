<template>
  <div class="search-page-container">
    <div class="search-form-container-main">
      <el-form :inline="true" :model="searchData" style="height: 70px; padding: 15px 0">
        <el-form-item
          id="inputKeywordFormItem"
          style="margin-bottom: 0; align-items: center; justify-items: center;">
          <template #label>
            <span style="font-weight: bold">{{ $t('search.keyword') }}</span>
          </template>
          <el-input
            v-model="inputKeyword" :placeholder="$t('search.keywordTip')"
            @keyup.enter="addKeyword" @blur="addKeyword"
            :style="{marginRight: '10px', width: keywordInputWidth}">
            <template #prefix>
              <div style="display: flex; flex-wrap: wrap; align-items: center;">
                <el-tag
                  v-for="(keyword, index) in searchData.keywords"
                  :key="index" @close="removeKeyword(index)"
                  size="small" style="margin-left: 0; margin-right: 5px; font-size: 14px;"
                  closable disable-transitions round>
                  {{ keyword }}
                </el-tag>
              </div>
            </template>

          </el-input>
        </el-form-item>

        <el-form-item style="margin-bottom: 0;">
          <template #label>
            <span style="font-weight: bold">{{ $t('search.timeRange') }}</span>
          </template>
          <el-date-picker
            v-model="searchData.date"
            type="daterange"
            :range-separator="$t('search.timeRangeSep')"
            :start-placeholder="$t('search.startTime')"
            :end-placeholder="$t('search.endTime')"
            value-format="YYYYMMDD"
            format="YYYY/MM/DD"
            :disabled-date="(date) => date.getTime() > Date.now()"
            clearable
          />
        </el-form-item>

        <el-form-item style="margin-bottom: 0;">
          <el-checkbox
            v-model="showSearchDetails"
            :label="$t('search.detailSearch')"
            size="large"
            style="margin-right: 10px;" />
        </el-form-item>

        <el-form-item style="margin-bottom: 0;">
          <el-checkbox
            v-model="queryInList"
            :label="$t('search.queryInList')"
            size="large"
            style="margin-right: 10px;" />
        </el-form-item>

        <el-form-item style="margin-bottom: 0;">
          <el-button type="primary" @click="onSubmit">{{ $t('search.query') }}</el-button>
        </el-form-item>
      </el-form>

      <div style="flex-grow: 1"></div>

      <div style="color: #a8abc3; margin-right: 20px;" v-show="searchData.total > 0">
        {{ $t('search.totalPre') + searchData.total + $t('search.totalPost') }}
      </div>

      <el-button v-show="!queryInList" type="primary" @click="addToListDialogVisible = true">
        {{ $t('search.addToList') }}
      </el-button>

      <!-- 确认添加数据到清单的对话框 -->
      <el-dialog
        width="30%"
        v-model="addToListDialogVisible"
        @close="addToListDialogVisible = false"
      >
        <template #header="{ close, titleId, titleClass }">
          <div class="my-header">
            <h4 :id="titleId" :class="titleClass">{{ $t('search.addToListTips.confirmTitle') }}</h4>
          </div>
        </template>
        <span>
          {{
            $t('search.addToListTips.confirmContent1') +
            String(searchData.total) +
            $t('search.addToListTips.confirmContent2')
          }}
        </span>
        <br />
        <br />
        <span
          v-show="searchData.total > maxToListCount" style="font-weight: bold">
          {{
            $t('search.addToListTips.confirmContent3') +
            String(maxToListCount) +
            $t('search.addToListTips.confirmContent4')
          }}
        </span>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="addToListDialogVisible = false">{{ $t('search.addToListTips.quitBtn') }}</el-button>
            <el-button type="primary" @click="addToList">{{ $t('search.addToListTips.confirmBtn') }}</el-button>
          </div>
        </template>

      </el-dialog>
    </div>

    <Transition name="height">
      <div class="search-form-container-details" v-show="showSearchDetails">
        <el-form :inline="true" :model="searchData" style="height: 70px; padding: 15px 0;">
          <el-form-item
            style="margin-bottom: 0; align-items: center; justify-items: center;">
            <template #label>
              <span style="font-weight: bold">{{ $t('search.keywordDetails') }}</span>
            </template>
            <div ref="caseSensitiveBox">
              <el-checkbox
                v-model="searchData.caseSensitive"
                :label="$t('search.caseSensitive')"
                size="large"
                style="margin-right: 10px;" />
            </div>
            <div ref="queryByContentBox">
              <el-checkbox
                v-model="searchData.queryByContent"
                :label="$t('search.queryContent')"
                size="large"
                style="margin-right: 10px;" />
            </div>
            <div ref="wordMatchBox">
              <el-checkbox
                v-model="searchData.wordMatch"
                :label="$t('search.wordMatch')"
                size="large" />
            </div>
          </el-form-item>

          <el-form-item style="margin-bottom: 0;">
            <template #label>
              <span style="font-weight: bold">{{ $t('search.source') }}</span>
            </template>

            <el-cascader
              style="width: 200px;"
              :options="sourceOptions"
              :props="{ multiple: true }"
              :placeholder="$t('search.sourceTip')"
              v-model="searchData.sources"
              collapse-tags
              collapse-tags-tooltip
              clearable />
          </el-form-item>

          <el-form-item style="margin-bottom: 0;">
            <template #label>
              <span style="font-weight: bold">{{ $t('search.contry') }}</span>
            </template>

            <el-cascader
              style="width: 150px;"
              :options="countryOptions"
              :placeholder="$t('search.contryTip')"
              v-model="searchData.country"
              collapse-tags
              collapse-tags-tooltip
              filterable
              clearable />
          </el-form-item>

          <el-form-item style="margin-bottom: 0;" v-if="true">
            <template #label>
              <span style="font-weight: bold">{{ $t('search.wordCount') }}</span>
            </template>
            <el-select
              v-model="searchData.wordCount"
              :placeholder="$t('search.wordCountTip')"
              style="width: 150px"
              clearable
            >
              <el-option
                v-for="item in wordCountRanges"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />

            </el-select>
          </el-form-item>

        </el-form>
      </div>
    </Transition>

    <div v-show="!updating && newsList.length < 1" style="height: calc(100vh - 70px - 40px);">
      <el-empty :description="t('search.empty')" :image-size="300" style="height: 100%; width: 100%;" />
    </div>

    <div
      class="news-cards-container"
      :style="{height: `calc(100vh - ${showSearchDetails ? '2' : '1'} * 70px - 40px)`, alignItems: 'flex-start'}"
      v-show="updating || newsList.length > 0"
      @wheel="updateNewsListScroll"
    >
      <div v-for="(item, index) in newsList" :key="index" class="news-card">
        <VNewCard :data="item" :keywords="searchData.keywords" />
      </div>
      <div class="loading-icon" v-show="updating">
        {{ $t('search.loading') }}
      </div>
    </div>

  </div>
</template>

<script lang="ts" setup>
import VNewCard from '../components/VNewCard.vue'
import { queryNews } from '@/utils/axiosUtil.js'
import { reactive, ref, onMounted, watch, computed, onBeforeMount } from 'vue'
import tippy, { animateFill } from 'tippy.js'
import 'tippy.js/dist/tippy.css'
import 'tippy.js/dist/backdrop.css'
import 'tippy.js/animations/shift-away.css'
import 'tippy.js/themes/light.css'
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'
import { ElNotification } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'

// region 获取今天的日期和30天前的日期

function formatDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0') // 月份从0开始，需加1
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

const today = new Date()
const thirtyDaysAgo = new Date()
thirtyDaysAgo.setDate(today.getDate() - 30)
const todayStr = formatDate(today)
const thirtyDaysAgoStr = formatDate(thirtyDaysAgo)

// endregion 获取今天的日期和30天前的日期

const { t, locale } = useI18n()
// 记录上一次查询的Search Data，添加清单时根据该数据查询
let lastSearchData = {
  keywords: [],
  caseSensitive: false,
  queryByContent: false,
  wordMatch: false,
  onlyId: false,
  date: [thirtyDaysAgoStr, todayStr],
  sources: [],
  country: '',
  wordCount: '',
  page: 1,
  limit: 30,
  total: 0
}
const searchData = reactive({
  keywords: [],
  caseSensitive: false,
  queryByContent: false,
  wordMatch: false,
  onlyId: false,
  date: [thirtyDaysAgoStr, todayStr],
  sources: [],
  country: '',
  wordCount: '',
  page: 1,
  limit: 30,
  total: 0
})
const store = useStore()
const route = useRoute()
const router = useRouter()
const wordCountRanges = [
  { value: [0, 1000], label: '≤1000' },
  { value: [1001, 3000], label: '>1000 && ≤3000' },
  { value: [3001, 5000], label: '>3000 && ≤5000' },
  { value: [5001, 99999999], label: '>5000' }
]

// region 高级搜索的Tooltips
const showSearchDetails = ref(false)
const caseSensitiveBox = ref(null)
const queryByContentBox = ref(null)
const wordMatchBox = ref(null)
const tooltipInstances = []

// 显示详细搜索
watch(showSearchDetails, (newValue) => {
  if (newValue) {
    if (tooltipInstances.length > 0) return
    // 增加tooltip
    const t1 = tippy(caseSensitiveBox.value, {
      theme: 'light',
      content: t('search.caseSensitiveTooltip'),
      placement: 'top',
      arrow: false,
      animateFill: true,
      plugins: [animateFill]
    })
    tooltipInstances.push(t1)
    const t2 = tippy(queryByContentBox.value, {
      theme: 'light',
      content: t('search.queryContentTooltip'),
      placement: 'top',
      arrow: false,
      animateFill: true,
      plugins: [animateFill]
    })
    tooltipInstances.push(t2)
    const t3 = tippy(wordMatchBox.value, {
      theme: 'light',
      content: t('search.wordMatchTooltip'),
      placement: 'top',
      arrow: false,
      animateFill: true,
      plugins: [animateFill]
    })
    tooltipInstances.push(t3)


  } else {
    // 清除查找设置
    searchData.caseSensitive = false
    searchData.queryByContent = false
    searchData.wordMatch = false
    searchData.wordCount = ''
    searchData.source = ''
  }
})

// 切换语言时更新Tooltip
watch(locale, () => {
  if (tooltipInstances.length !== 3) return
  tooltipInstances[0].setContent(t('search.caseSensitiveTooltip'))
  tooltipInstances[1].setContent(t('search.queryContentTooltip'))
  tooltipInstances[2].setContent(t('search.wordMatchTooltip'))
})

// endregion 高级搜索的Tooltips

const sourceOptions = [
  { value: 'yorkpress', label: 'yorkpress' },
  { value: 'nytimes', label: 'nytimes' },
  { value: 'dw', label: 'dw' },
  { value: 'yahoo', label: 'yahoo' },
  { value: 'washingtonpost', label: 'washingtonpost' },
  { value: 'theguardian', label: 'theguardian' },
  { value: 'tass', label: 'tass' },
  { value: 'apnews', label: 'apnews' },
  { value: 'apr', label: 'apr' },
  { value: 'bbc', label: 'bbc' },
  { value: 'bignewsnetwork', label: 'bignewsnetwork' },
  { value: 'cnn', label: 'cnn' },
  { value: 'dailymail', label: 'dailymail' },
  { value: 'foxnews', label: 'foxnews' },
  { value: 'globalsecurity', label: 'globalsecurity' },
  { value: 'indiablooms', label: 'indiablooms' },
  { value: 'indiaexpress', label: 'indiaexpress' },
  { value: 'jpost', label: 'jpost' },
  { value: 'mirror', label: 'mirror' },
  { value: 'africa', label: 'africa' },
  { value: 'france24', label: 'france24' },
  { value: 'abcnews', label: 'abcnews' },
  { value: 'thesun', label: 'thesun' },
  { value: 'economist', label: 'economist' }
]

const countryOptions = computed(() => [
  { value: 'AFG', label: t('countrys.Afghanistan') },
  { value: 'ALB', label: t('countrys.Albania') },
  { value: 'DZA', label: t('countrys.Algeria') },
  { value: 'AND', label: t('countrys.Andorra') },
  { value: 'AGO', label: t('countrys.Angola') },
  { value: 'ARG', label: t('countrys.Argentina') },
  { value: 'ARM', label: t('countrys.Armenia') },
  { value: 'AUS', label: t('countrys.Australia') },
  { value: 'AUT', label: t('countrys.Austria') },
  { value: 'AZE', label: t('countrys.Azerbaijan') },
  { value: 'BHS', label: t('countrys.Bahamas') },
  { value: 'BHR', label: t('countrys.Bahrain') },
  { value: 'BGD', label: t('countrys.Bangladesh') },
  { value: 'BRB', label: t('countrys.Barbados') },
  { value: 'BLR', label: t('countrys.Belarus') },
  { value: 'BEL', label: t('countrys.Belgium') },
  { value: 'BLZ', label: t('countrys.Belize') },
  { value: 'BEN', label: t('countrys.Benin') },
  { value: 'BTN', label: t('countrys.Bhutan') },
  { value: 'BOL', label: t('countrys.Bolivia') },
  { value: 'BIH', label: t('countrys.Bosnia_and_Herzegovina') },
  { value: 'BWA', label: t('countrys.Botswana') },
  { value: 'BRA', label: t('countrys.Brazil') },
  { value: 'BRN', label: t('countrys.Brunei') },
  { value: 'BGR', label: t('countrys.Bulgaria') },
  { value: 'BFA', label: t('countrys.Burkina_Faso') },
  { value: 'BDI', label: t('countrys.Burundi') },
  { value: 'CPV', label: t('countrys.Cabo_Verde') },
  { value: 'KHM', label: t('countrys.Cambodia') },
  { value: 'CMR', label: t('countrys.Cameroon') },
  { value: 'CAN', label: t('countrys.Canada') },
  { value: 'CAF', label: t('countrys.Central_African_Republic') },
  { value: 'TCD', label: t('countrys.Chad') },
  { value: 'CHL', label: t('countrys.Chile') },
  { value: 'CHN', label: t('countrys.China') },
  { value: 'COL', label: t('countrys.Colombia') },
  { value: 'COM', label: t('countrys.Comoros') },
  { value: 'COG', label: t('countrys.Congo') },
  { value: 'CRI', label: t('countrys.Costa_Rica') },
  { value: 'CIV', label: t('countrys.Cote_d_Ivoire') },
  { value: 'HRV', label: t('countrys.Croatia') },
  { value: 'CUB', label: t('countrys.Cuba') },
  { value: 'CYP', label: t('countrys.Cyprus') },
  { value: 'CZE', label: t('countrys.Czech_Republic') },
  { value: 'COD', label: t('countrys.Democratic_Republic_of_the_Congo') },
  { value: 'DNK', label: t('countrys.Denmark') },
  { value: 'DJI', label: t('countrys.Djibouti') },
  { value: 'DMA', label: t('countrys.Dominica') },
  { value: 'DOM', label: t('countrys.Dominican_Republic') },
  { value: 'ECU', label: t('countrys.Ecuador') },
  { value: 'EGY', label: t('countrys.Egypt') },
  { value: 'SLV', label: t('countrys.El_Salvador') },
  { value: 'GNQ', label: t('countrys.Equatorial_Guinea') },
  { value: 'ERI', label: t('countrys.Eritrea') },
  { value: 'EST', label: t('countrys.Estonia') },
  { value: 'SWZ', label: t('countrys.Eswatini') },
  { value: 'ETH', label: t('countrys.Ethiopia') },
  { value: 'FJI', label: t('countrys.Fiji') },
  { value: 'FIN', label: t('countrys.Finland') },
  { value: 'FRA', label: t('countrys.France') },
  { value: 'GAB', label: t('countrys.Gabon') },
  { value: 'GMB', label: t('countrys.Gambia') },
  { value: 'GEO', label: t('countrys.Georgia') },
  { value: 'DEU', label: t('countrys.Germany') },
  { value: 'GHA', label: t('countrys.Ghana') },
  { value: 'GRC', label: t('countrys.Greece') },
  { value: 'GRD', label: t('countrys.Grenada') },
  { value: 'GTM', label: t('countrys.Guatemala') },
  { value: 'GIN', label: t('countrys.Guinea') },
  { value: 'GNB', label: t('countrys.Guinea_Bissau') },
  { value: 'GUY', label: t('countrys.Guyana') },
  { value: 'HTI', label: t('countrys.Haiti') },
  { value: 'HND', label: t('countrys.Honduras') },
  { value: 'HUN', label: t('countrys.Hungary') },
  { value: 'ISL', label: t('countrys.Iceland') },
  { value: 'IND', label: t('countrys.India') },
  { value: 'IDN', label: t('countrys.Indonesia') },
  { value: 'IRN', label: t('countrys.Iran') },
  { value: 'IRQ', label: t('countrys.Iraq') },
  { value: 'IRL', label: t('countrys.Ireland') },
  { value: 'ISR', label: t('countrys.Israel') },
  { value: 'ITA', label: t('countrys.Italy') },
  { value: 'JAM', label: t('countrys.Jamaica') },
  { value: 'JPN', label: t('countrys.Japan') },
  { value: 'JOR', label: t('countrys.Jordan') },
  { value: 'KAZ', label: t('countrys.Kazakhstan') },
  { value: 'KEN', label: t('countrys.Kenya') },
  { value: 'KIR', label: t('countrys.Kiribati') },
  { value: 'PRK', label: t('countrys.North_Korea') },
  { value: 'KOR', label: t('countrys.South_Korea') },
  { value: 'KWT', label: t('countrys.Kuwait') },
  { value: 'KGZ', label: t('countrys.Kyrgyzstan') },
  { value: 'LAO', label: t('countrys.Laos') },
  { value: 'LVA', label: t('countrys.Latvia') },
  { value: 'LBN', label: t('countrys.Lebanon') },
  { value: 'LSO', label: t('countrys.Lesotho') },
  { value: 'LBR', label: t('countrys.Liberia') },
  { value: 'LBY', label: t('countrys.Libya') },
  { value: 'LIE', label: t('countrys.Liechtenstein') },
  { value: 'LTU', label: t('countrys.Lithuania') },
  { value: 'LUX', label: t('countrys.Luxembourg') },
  { value: 'MDG', label: t('countrys.Madagascar') },
  { value: 'MWI', label: t('countrys.Malawi') },
  { value: 'MYS', label: t('countrys.Malaysia') },
  { value: 'MDV', label: t('countrys.Maldives') },
  { value: 'MLI', label: t('countrys.Mali') },
  { value: 'MLT', label: t('countrys.Malta') },
  { value: 'MHL', label: t('countrys.Marshall_Islands') },
  { value: 'MRT', label: t('countrys.Mauritania') },
  { value: 'MUS', label: t('countrys.Mauritius') },
  { value: 'MEX', label: t('countrys.Mexico') },
  { value: 'FSM', label: t('countrys.Micronesia') },
  { value: 'MDA', label: t('countrys.Moldova') },
  { value: 'MCO', label: t('countrys.Monaco') },
  { value: 'MNG', label: t('countrys.Mongolia') },
  { value: 'MNE', label: t('countrys.Montenegro') },
  { value: 'MAR', label: t('countrys.Morocco') },
  { value: 'MOZ', label: t('countrys.Mozambique') },
  { value: 'MMR', label: t('countrys.Myanmar') },
  { value: 'NAM', label: t('countrys.Namibia') },
  { value: 'NRU', label: t('countrys.Nauru') },
  { value: 'NPL', label: t('countrys.Nepal') },
  { value: 'NLD', label: t('countrys.Netherlands') },
  { value: 'NZL', label: t('countrys.New_Zealand') },
  { value: 'NIC', label: t('countrys.Nicaragua') },
  { value: 'NER', label: t('countrys.Niger') },
  { value: 'NGA', label: t('countrys.Nigeria') },
  { value: 'MKD', label: t('countrys.North_Macedonia') },
  { value: 'NOR', label: t('countrys.Norway') },
  { value: 'OMN', label: t('countrys.Oman') },
  { value: 'PAK', label: t('countrys.Pakistan') },
  { value: 'PLW', label: t('countrys.Palau') },
  { value: 'PAN', label: t('countrys.Panama') },
  { value: 'PNG', label: t('countrys.Papua_New_Guinea') },
  { value: 'PRY', label: t('countrys.Paraguay') },
  { value: 'PER', label: t('countrys.Peru') },
  { value: 'PHL', label: t('countrys.Philippines') },
  { value: 'POL', label: t('countrys.Poland') },
  { value: 'PRT', label: t('countrys.Portugal') },
  { value: 'QAT', label: t('countrys.Qatar') },
  { value: 'ROU', label: t('countrys.Romania') },
  { value: 'RUS', label: t('countrys.Russia') },
  { value: 'RWA', label: t('countrys.Rwanda') },
  { value: 'KNA', label: t('countrys.Saint_Kitts_and_Nevis') },
  { value: 'LCA', label: t('countrys.Saint_Lucia') },
  { value: 'VCT', label: t('countrys.Saint_Vincent_and_the_Grenadines') },
  { value: 'WSM', label: t('countrys.Samoa') },
  { value: 'SMR', label: t('countrys.San_Marino') },
  { value: 'STP', label: t('countrys.Sao_Tome_and_Principe') },
  { value: 'SAU', label: t('countrys.Saudi_Arabia') },
  { value: 'SEN', label: t('countrys.Senegal') },
  { value: 'SRB', label: t('countrys.Serbia') },
  { value: 'SYC', label: t('countrys.Seychelles') },
  { value: 'SLE', label: t('countrys.Sierra_Leone') },
  { value: 'SGP', label: t('countrys.Singapore') },
  { value: 'SVK', label: t('countrys.Slovakia') },
  { value: 'SVN', label: t('countrys.Slovenia') },
  { value: 'SLB', label: t('countrys.Solomon_Islands') },
  { value: 'SOM', label: t('countrys.Somalia') },
  { value: 'ZAF', label: t('countrys.South_Africa') },
  { value: 'SSD', label: t('countrys.South_Sudan') },
  { value: 'ESP', label: t('countrys.Spain') },
  { value: 'LKA', label: t('countrys.Sri_Lanka') },
  { value: 'SDN', label: t('countrys.Sudan') },
  { value: 'SUR', label: t('countrys.Suriname') },
  { value: 'SWE', label: t('countrys.Sweden') },
  { value: 'CHE', label: t('countrys.Switzerland') },
  { value: 'SYR', label: t('countrys.Syria') },
  { value: 'TWN', label: t('countrys.Taiwan') },
  { value: 'TJK', label: t('countrys.Tajikistan') },
  { value: 'TZA', label: t('countrys.Tanzania') },
  { value: 'THA', label: t('countrys.Thailand') },
  { value: 'TLS', label: t('countrys.Timor_Leste') },
  { value: 'TGO', label: t('countrys.Togo') },
  { value: 'TON', label: t('countrys.Tonga') },
  { value: 'TTO', label: t('countrys.Trinidad_and_Tobago') },
  { value: 'TUN', label: t('countrys.Tunisia') },
  { value: 'TUR', label: t('countrys.Turkey') },
  { value: 'TKM', label: t('countrys.Turkmenistan') },
  { value: 'TUV', label: t('countrys.Tuvalu') },
  { value: 'UGA', label: t('countrys.Uganda') },
  { value: 'UKR', label: t('countrys.Ukraine') },
  { value: 'ARE', label: t('countrys.United_Arab_Emirates') },
  { value: 'GBR', label: t('countrys.UK') },
  { value: 'USA', label: t('countrys.USA') },
  { value: 'URY', label: t('countrys.Uruguay') },
  { value: 'UZB', label: t('countrys.Uzbekistan') },
  { value: 'VUT', label: t('countrys.Vanuatu') },
  { value: 'VEN', label: t('countrys.Venezuela') },
  { value: 'VNM', label: t('countrys.Vietnam') },
  { value: 'YEM', label: t('countrys.Yemen') },
  { value: 'ZMB', label: t('countrys.Zambia') },
  { value: 'ZWE', label: t('countrys.Zimbabwe') }
])

onBeforeMount(() => document.title = 'Search')

// region 查询新闻
const queryInList = ref(false)
const newsList = ref([])
const updating = ref(false)
// 根据参数判断是否查询清单内容
onBeforeMount(() => {
  if (route.params.queryInList !== undefined)
    queryInList.value = JSON.parse(route.params.queryInList)
  else queryInList.value = false
})
// 跳转到该网页时，请求第一页数据
onMounted(async () => await getNews(searchData))
// 请求后端新闻文章
const getNews = async (data) => {
  if (updating.value) return // 不重复请求数据
  updating.value = true
  const configData = { ...data }
  lastSearchData = { ...data }
  // 如果勾选只查询清单内容，则传输ids列表
  if (queryInList.value)
    configData.ids = [...store.state.analysisNewsIds]
  console.log(new Date(), '开始请求数据')
  await queryNews(configData).then(res => {
    if (res.code === 0) {
      // 将数据加入列表，用于显示
      newsList.value.push(...res.data['newsList'])
      data.total = res.data['totalRecords']
    }
  })
  updating.value = false
  console.log(new Date(), '请求数据成功')
}

// 修改route参数时重新请求数据
watch(() => route.params.queryInList, (newValue) => queryInList.value = JSON.parse(newValue))
// 选择只查询清单内容时重新请求数据
watch(queryInList, async () => {
  searchData.total = 0
  newsList.value.length = 0
  searchData.page = 1
  await getNews(searchData)
})
// 滚动时请求新数据
const updateNewsListScroll = async (event) => {
  if (updating.value || newsList.value.length >= searchData.total) return

  const element = event.currentTarget
  const scrollHeight = element.scrollHeight
  const scrollTop = element.scrollTop
  const clientHeight = element.clientHeight
  if (clientHeight + scrollTop >= scrollHeight - 500) {
    searchData.page++
    await getNews(searchData, false)
  }
}
// 点击查询按钮
const onSubmit = async () => {
  searchData.total = 0
  newsList.value.length = 0 // 清空新闻列表
  searchData.page = 1 // 将页码修改为第一页
  await getNews(searchData)
}
// endregion 请求数据

// region 将查询到的所有新闻加入清单
const maxToListCount = ref(5000)
const addToListDialogVisible = ref(false)
const addToList = async () => {
  addToListDialogVisible.value = false
  if (updating.value) {
    ElNotification({
      title: t('search.notifications.error.title'),
      message: t('search.notifications.error.message'),
      type: 'error',
      duration: 1500
    })
    return
  }
  // 弹出提示框
  const waitingNotification = ElNotification({
    title: t('search.notifications.wait.title'),
    message: t('search.notifications.wait.message'),
    type: 'info',
    duration: 0
  })
  // 修改Search Data，以获取所有新闻数据
  lastSearchData.page = 1
  lastSearchData.limit = Math.min(searchData.total, maxToListCount.value)
  lastSearchData.onlyId = true
  // 请求
  updating.value = true
  const configData = { ...lastSearchData }
  console.log(new Date(), '开始请求数据')
  await queryNews(configData).then(res => {
    if (res.code === 0) {
      store.commit('appendAnalysisNewsIds', res.data['ids'])
      lastSearchData.total = res.data['totalRecords']
      // 完成请求，弹出提示框
      waitingNotification.close()
      ElNotification({
        title: t('search.notifications.success.title'),
        message: t('search.notifications.success.message1') +
          String(Math.min(lastSearchData.total, maxToListCount.value)) +
          t('search.notifications.success.message2'),
        type: 'success',
        duration: 1500
      })
    }
  })
  // 结束请求
  updating.value = false
  waitingNotification.close()
}
// endregion

// region 显示文本框关键词
// 文本框按下回车后添加关键词
const inputKeyword = ref('')
const addKeyword = () => {
  if (inputKeyword.value === '') return
  if (searchData.keywords.findIndex(item => item === inputKeyword.value) !== -1) return
  searchData.keywords.push(inputKeyword.value)
  inputKeyword.value = ''
}

// 固定关键词搜索输入框长度
const defaultKeywordInputWidth = 200
const keywordInputWidth = computed(() => {
  const prefixDom = document.querySelector('.inputKeyword .el-input__prefix')
  if (prefixDom === null) return defaultKeywordInputWidth
  const prefixWidth = parseInt(prefixDom.style.width)
  return defaultKeywordInputWidth + prefixWidth
})

// 点击标签的×，删除对应的关键词
const removeKeyword = (index) => searchData.keywords.splice(index, 1)
// endregion 显示文本框关键词

// region 为关键词输入框添加提示
let inputKeywordTippy = null
onMounted(() => {
  const inputKeywordFormItem = document.querySelector('#inputKeywordFormItem')
  inputKeywordTippy = tippy(inputKeywordFormItem, {
    theme: 'light',
    content: t('search.keywordTooltip'),
    placement: 'bottom',
    arrow: false,
    animateFill: true,
    hideOnClick: false,
    plugins: [animateFill]
  })
})

watch(locale, () => {
  if (inputKeywordTippy === null) return
  inputKeywordTippy.setContent(t('search.keywordTooltip'))
})
// endregion 为关键词输入框添加提示

</script>

<style scoped lang="scss">
@import "public/styles/variables";

.search-page-container {
  font-family: "Inter", sans-serif;

  padding: 0 25px;
  width: 100%;
  height: calc(100vh - $navbar-height);

  .search-form-container-main {
    width: 100%;
    padding: 0 5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .search-form-container-details {
    width: 100%;
    padding: 0 5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .news-cards-container {
    width: 100%;
    overflow-y: auto;
    padding-right: 15px;

    .news-card {
      width: 20%;
      display: inline-block;
      padding: 5px;
      margin: 0;
      box-sizing: border-box;
    }

    .loading-icon {
      width: 100%;
      text-align: center;
      margin: 0;
      padding: 20px 0;
      color: #a8abc3;
      box-sizing: border-box;
    }
  }

  .news-cards-container::-webkit-scrollbar {
    width: 10px;
  }
}

.demo-pagination-block {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.height-enter-active, .height-leave-active {
  transition: height 0.5s ease, opacity 0.5s ease;;
}

.height-enter-from, .height-leave-to {
  height: 0;
  opacity: 0;
}

.height-enter-to, .height-leave-from {
  height: 70px;
  opacity: 1;
}

</style>
