(function() {
    "use strict";
    mainSDPApp.factory("documentsControllerService", ["$http", function(n) {
        return {
            loadAllWeeksPerTerms: function(t, i) {
                var r = appGlobalSettings.ResourceServerURL + "/school/allweeksperterms?schoolId=" + t + "&selectedTerms=" + i;
                return n.get(r)
            },
            createSession: function(t, i, r, u, f) {
                var e = {
                    quizId: t,
                    quizLevelSectionId: i,
                    AccountId: r,
                    quizCourseId: u,
                    quizCourseGroupId: f
                }
                  , o = appGlobalSettings.SessionPlayerServerURL + "/quizzes/quizSession?";
                return n.post(o, e)
            },
            createPeriodicSession: function(t, i, r, u) {
                var f = {
                    QuizId: t,
                    practiceItems: i,
                    quizCourseId: r,   
                    quizCourseGroupId: u
                }
                  , e = appGlobalSettings.SessionPlayerServerURL + "/quizzes/practiceSession?";
                return n.post(e, f)
            },
            saveQuizSession: function(t, i, r) {
                var u = appGlobalSettings.SessionPlayerServerURL + "/quizzes/sessions/save?selectedQuizSessionId=" + t + "&statusId=" + i + "&currentStatus=" + r;
                return n.post(u, null, {
                    skipInterceptorHandling: !0
                })
            },
            checkSessionTimePassed: function(t, i, r, u) {
                var f = appGlobalSettings.SessionPlayerServerURL + "/quizzes/sessions/is-time-passed?quizId=" + t + "&quizSessionId=" + i + "&quizCourseId=" + r + "&quizCourseGroupId=" + u;
                return n.post(f, null, {
                    skipInterceptorHandling: !0
                })
            },
            saveSessionCourses: function(t) {
                var i = appGlobalSettings.ResourceServerURL + "/onlineQuiz/quizSessionCourses?sessionId=" + t;
                return n.post(i)
            },
            checkSessionLockStatus: function(t) {
                var i = appGlobalSettings.SessionPlayerServerURL + "/quizzes/session-lock-status?quizId=" + t;
                return n.get(i)
            }
        }
    }
    ]).controller("DocumentsController", ["documentsControllerService", "$http", "$window", "$timeout", "$scope", "$q", "sharedDataService", "$filter", function(n, t, i, r, u, f, e, o) {
        var s = this;
        this.allTerms = [];
        this.allWeeks = [];
        this.allSubjects = [];
        this.textToHighlight = "";
        this.docId = -1;
        this.docCode = -1;
        this.isLoading = !0;
        this.documents = [];
        this.periodicQ = [];
        this.currentTermWeek = null;
        this.selectedTerms = [];
        this.selectedWeeks = [];
        this.selectedWeeksLabel = "";
        this.arrSelectedWeeksDescription = [];
        this.selectedSchoolId = SDPUtility.getQueryStringValue("scid");
        this.studentAccountId = -1;
        this.documentsRequestTimeout = f.defer();
        this.selectedDoc = -1;
        this.termFilter = !1;
        this.weekFilter = !1;
        this.subjectFilter = !1;
        this.selectAllTerms = !1;
        this.selectAllWeeks = !1;
        this.selectAllSubjects = !0;
        this.termFilterClassOpen = !1;
        this.termFilterClassData = !0;
        this.weekFilterClassOpen = !1;
        this.weekFilterClassData = !0;
        this.subjectFilterClassOpen = !1;
        this.subjectFilterClassData = !0;
        this.readUnreadDocuments = !1;
        this.selectCurrentTermWeek = !1;
        this.hideTermWeekFilters = !1;
        this.hideFilterOptions = !1;
        this.hideFilterDocumentsOptions = !1;
        this.menuId = -1;
        this.Cdn = appGlobalSettings.CDNPath;
        this.isPopupOpen = !1;
        this.popupOnlineQuizModelCenter = [];
        this.viewHistoryCheckbox = "viewHistoryRdb";
        this.newQuizCheckbox = "newQuiz";
        this.acadYear = -1;
        this.hideBooks = !1;
        this.viewUnreadDocumentsLabel = "View Unread Documents";
        this.documentsFound = !1;
        this.selectedSections = [];
        this.isActive = !1;
        this.maxAttemptsExeededId = "BC3djp%2F56bY%3D";
        this.initialize = function() {
            u.$watch("menuId", function(n) {
                n !== undefined && n !== s.menuId && (s.menuId = n)
            });
            u.$watch("studentAccountId", function(n) {
                n !== undefined && n !== s.studentAccountId && (s.studentAccountId = n,
                s.selectedDoc == -1 || s.studentAccountId === "-1" || s.docId != s.selectedDoc || s.isLoading || (s.resetVariables(),
                s.loadDocuments(s.docId, s.studentAccountId, s.acadYear, !1)))
            });
            u.$watch("docId", function(n) {
                n !== undefined && n !== s.docId && (s.docId = n)
            });
            u.$watch("docCode", function(n) {
                n !== undefined && n !== s.docCode && (s.docCode = n)
            });
            u.$watch("selectedDoc", function(n) {
                n !== undefined && n !== s.selectedDoc && (s.selectedDoc = n,
                s.selectedDoc !== "-1" && s.studentAccountId !== "-1" && s.docId == s.selectedDoc && (s.resetVariables(),
                s.loadDocuments(s.docId, s.studentAccountId, s.acadYear, !1)))
            });
            u.$watch("highlightText", function(n) {
                n !== undefined && n !== s.textToHighlight && (s.textToHighlight = n)
            });
            u.$emit("mobileSearchClicked", !0)
        }
        ;
        this.showFilter = function() {
            (s.docCode == "-99" || s.docCode == "5") && (s.hideFilterOptions = !0)
        }
        ;
        this.loadDocuments = function(n, i, r, u) {
            var f = [], e;
            s.isLoading = !0;
            e = apiUrls.getTermsAndCurrentTermWeekPath();
            t.get(e).then(function(n) {
                var e, h;
                f = n.data;
                s.currentTermWeek = f.CurrentWeek;
                e = !1;
                angular.forEach(f.Terms, function(n) {
                    e = !1;
                    s.menuId == 80 && s.docCode != 5 ? (e = !0,
                    s.selectedTerms.push(n.Term)) : s.currentTermWeek.Term === n.Term && (s.termFilterClassData = !0,
                    e = !0,
                    s.selectedTerms.push(n.Term));
                    s.allTerms.push({
                        Term: n.Term,
                        Checked: e
                    })
                });
                h = "";
                s.docCode != "-99" ? (h = apiUrls.getDownloadsNewUri(i, -1, s.docId, s.menuId, r),
                t.get(h, {
                    timeout: s.documentsRequestTimeout.promise
                }).then(function(n) {
                    var r = [], f = [], e, h, c;
                    if (n.data != undefined && n.data != null && n.data.length > 0) {
                        for (r = n.data,
                        e = 0; e < r.length; e++)
                            r[e].UploadedDate = new Date(r[e].UploadedDate),
                            r[e].Display = !1;
                        r.sort(function(n, t) {
                            return n.TermWeek.WeekNumber > t.TermWeek.WeekNumber
                        });
                        s.documents = r
                    }
                    h = u;
                    s.docCode == 4 ? (s.hideTermWeekFilters = !1,
                    s.hideFilterDocumentsOptions = !1,
                    (s.selectedWeeks == null || s.selectedWeeks.length == 0) && (s.selectedWeeks = s.currentTermWeek.TermWeek),
                    s.loadAllWeeksPerTerms(s.selectedSchoolId, s.selectedTerms, s.currentTermWeek.TermWeek, !0, function() {
                        s.loadAMSQuiz(!1)
                    })) : s.docCode == 8 ? (s.hideTermWeekFilters = !0,
                    s.hideFilterDocumentsOptions = !0,
                    c = apiUrls.getCoursePracticeQuizUri(i),
                    t.get(c).then(function(n) {
                        var i, t;
                        for (f = n.data,
                        i = {},
                        t = 0; t < f.length; t++)
                            f[t].UploadedDate = new Date(f[t].UploadedDate),
                            f[t].SubmitDate = o("date")(f[t].SubmitDate, "MMM dd, yyyy");
                        angular.forEach(f, function(n) {
                            var i = s.documents.filter(t=>t.Name == n.Name), t, r;
                            i != null && i.length > 0 ? (t = i[0].Book.filter(t=>t.BookNumber == n.QuizQuestion.QuestionCurriculum.Book),
                            t != null && t.length > 0 ? (r = t[0].Chapter.filter(i=>t[0].BookNumber == n.QuizQuestion.QuestionCurriculum.Book && i.ChapterNo == n.QuizQuestion.QuestionCurriculum.Chapter),
                            r != null && r.length > 0 ? r[0].Section.push({
                                PKForSync: n.QuizQuestion.QuestionCurriculum.PKForSync,
                                SectionNo: n.QuizQuestion.QuestionCurriculum.Section,
                                SectionDescription: n.QuizQuestion.QuestionCurriculum.SectionDescription,
                                Checked: !n.PracticeBySection
                            }) : t[0].Chapter.push({
                                ChapterNo: n.QuizQuestion.QuestionCurriculum.Chapter,
                                ChapterDescription: n.QuizQuestion.QuestionCurriculum.ChapterDescription,
                                Checked: !n.PracticeBySection,
                                Section: [{
                                    PKForSync: n.QuizQuestion.QuestionCurriculum.PKForSync,
                                    SectionNo: n.QuizQuestion.QuestionCurriculum.Section,
                                    SectionDescription: n.QuizQuestion.QuestionCurriculum.SectionDescription,
                                    Checked: !n.PracticeBySection
                                }]
                            })) : i[0].Book.push({
                                BookNumber: n.QuizQuestion.QuestionCurriculum.Book,
                                BookDescription: n.QuizQuestion.QuestionCurriculum.BookDescription,
                                Checked: !n.PracticeBySection,
                                Chapter: [{
                                    ChapterNo: n.QuizQuestion.QuestionCurriculum.Chapter,
                                    ChapterDescription: n.QuizQuestion.QuestionCurriculum.ChapterDescription,
                                    Checked: !n.PracticeBySection,
                                    Section: [{
                                        PKForSync: n.QuizQuestion.QuestionCurriculum.PKForSync,
                                        SectionNo: n.QuizQuestion.QuestionCurriculum.Section,
                                        SectionDescription: n.QuizQuestion.QuestionCurriculum.SectionDescription,
                                        Checked: !n.PracticeBySection
                                    }]
                                }]
                            })) : s.documents.push({
                                CategoryId: 48,
                                Display: !0,
                                DocumentSchoolLinkId: 0,
                                DownloadDocumentId: 0,
                                DownloadedSchoolDestinationId: 0,
                                IsRead: !1,
                                Name: n.Name,
                                Description: n.Description == "" ? n.Name : n.Description,
                                Path: "",
                                Size: 0,
                                SizeUnit: "",
                                SubSubject: {
                                    SubSubjectId: 0,
                                    Name: "",
                                    Subject: {
                                        Code: n.QuizSubject.Subject.Code,
                                        CoreSubjectId: 2,
                                        Name: n.QuizSubject.Subject.Name
                                    }
                                },
                                SubSubjectId: 0,
                                Book: [{
                                    BookNumber: n.QuizQuestion.QuestionCurriculum.Book,
                                    BookDescription: n.QuizQuestion.QuestionCurriculum.BookDescription,
                                    Checked: !n.PracticeBySection,
                                    Chapter: [{
                                        ChapterNo: n.QuizQuestion.QuestionCurriculum.Chapter,
                                        ChapterDescription: n.QuizQuestion.QuestionCurriculum.ChapterDescription,
                                        Checked: !n.PracticeBySection,
                                        Section: [{
                                            PKForSync: n.QuizQuestion.QuestionCurriculum.PKForSync,
                                            SectionNo: n.QuizQuestion.QuestionCurriculum.Section,
                                            SectionDescription: n.QuizQuestion.QuestionCurriculum.SectionDescription,
                                            Checked: !n.PracticeBySection
                                        }]
                                    }]
                                }],
                                PracticeBySection: n.PracticeBySection,
                                TermWeek: {
                                    Term: n.QuizTermWeek.Term,
                                    WeekNumber: n.QuizTermWeek.Week,
                                    WeekDescriptionValue: n.QuizTermWeek.WeekDescriptionValue
                                },
                                UploadedDate: new Date(n.UploadedDate),
                                OnlineQuizObject: n
                            })
                        });
                        s.loadAllSubjects();
                        s.loadFilterData(s.readUnreadDocuments);
                        angular.forEach(s.documents, function(n) {
                            n.Display = !0
                        })
                    })) : (s.hideTermWeekFilters = !1,
                    s.hideFilterDocumentsOptions = !1,
                    s.docCode == 5 ? s.loadAllWeeksPerTerms(s.selectedSchoolId, s.currentTermWeek.Term, s.currentTermWeek.TermWeek, h) : s.loadAllWeeksPerTerms(s.selectedSchoolId, s.currentTermWeek.Term, s.currentTermWeek.TermWeek, h))
                })) : (h = apiUrls.getStudentSessionsPath(i, -1, 80),
                t.get(h, {
                    timeout: s.documentsRequestTimeout.promise
                }).then(function(n) {
                    var t, i;
                    if (n.data != undefined && n.data != null && n.data.length > 0) {
                        for (t = n.data,
                        i = 0; i < t.length; i++)
                            t[i].UploadedDate = new Date(t[i].UploadedDate);
                        t.length > 0 && t.sort(function(n, t) {
                            return n.TermWeek.WeekNumber > t.TermWeek.WeekNumber
                        });
                        s.documents = t
                    }
                    s.loadAllWeeksPerTerms(s.selectedSchoolId, s.currentTermWeek.Term, s.currentTermWeek.TermWeek, !1)
                }))
            })
        }
        ;
        this.loadAMSQuiz = function(n) {
            var i = []
              , r = apiUrls.getOnlineQuizUri(s.studentAccountId, s.selectedTerms, s.selectedWeeks);
            t.get(r).then(function(t) {
                var u, r;
                for (i = t.data,
                u = {},
                r = 0; r < i.length; r++)
                    i[r].UploadedDate = new Date(i[r].UploadedDate),
                    i[r].SubmitDate = o("date")(i[r].SubmitDate, "MMM dd, yyyy");
                angular.forEach(i, function(n) {
                    var t = s.documents.filter(t=>t.CategoryId == 45 && t.OnlineQuizObject != null && t.OnlineQuizObject.ID == n.ID);
                    t.length > 0 && s.documents.splice(s.documents.indexOf(t[0]), 1);
                    s.documents.push({
                        CategoryId: 45,
                        Display: !1,
                        DocumentSchoolLinkId: 0,
                        DownloadDocumentId: 0,
                        DownloadedSchoolDestinationId: 0,
                        IsRead: !1,
                        Name: n.Description == "" ? n.Name : n.Description,
                        Description: n.Description == "" ? n.Name : n.Description,
                        Path: "",
                        Size: 0,
                        SizeUnit: "",
                        SubSubject: {
                            SubSubjectId: 0,
                            Name: "",
                            Subject: {
                                Code: n.QuizSubject.Subject.Code,
                                CoreSubjectId: 2,
                                Name: n.QuizSubject.Subject.Name
                            }
                        },
                        SubSubjectId: 0,
                        TermWeek: {
                            Term: n.QuizTermWeek.Term,
                            WeekNumber: n.QuizTermWeek.Week,
                            WeekDescriptionValue: n.QuizTermWeek.WeekDescriptionValue
                        },
                        UploadedDate: new Date(n.UploadedDate),
                        OnlineQuizObject: n
                    })
                });
                n ? s.loadAllWeeksPerTerms(s.selectedSchoolId, s.currentTermWeek.Term, s.currentTermWeek.TermWeek, n) : (s.loadAllSubjects(),
                s.loadFilterData(s.readUnreadDocuments))
            })
        }
        ;
        this.GetAvailability = function(n) {
            var i = 0, t = new Date, e = t.getUTCFullYear() + "-" + (t.getUTCMonth() + 1) + "-" + t.getUTCDate() + " " + t.getUTCHours() + ":" + t.getUTCMinutes() + ":" + t.getUTCSeconds(), r = new Date(e), u, f;
            return n.QuizStart == "0001-01-01T00:00:00" && n.QuizEnd == "0001-01-01T00:00:00" ? i = 0 : n.QuizStart != "0001-01-01T00:00:00" && n.QuizEnd == "0001-01-01T00:00:00" ? (u = new Date(n.QuizStart),
            i = u > r ? 1 : 0) : n.QuizStart == "0001-01-01T00:00:00" && n.QuizEnd != "0001-01-01T00:00:00" ? (f = new Date(n.QuizEnd),
            i = r > f ? 1 : 0) : n.QuizStart != "0001-01-01T00:00:00" && n.QuizEnd != "0001-01-01T00:00:00" && (u = new Date(n.QuizStart),
            f = new Date(n.QuizEnd),
            i = r > u && r < f ? 0 : 1),
            i
        }
        ;
        this.loadAllSubjects = function() {
            s.docCode != "-99" ? angular.forEach(s.documents, function(n) {
                var t = s.inArray(s.allSubjects, n.SubSubject.Subject.Code);
                t || s.allSubjects.push({
                    Code: n.SubSubject.Subject.Code,
                    Name: n.SubSubject.Subject.Name,
                    Checked: !0
                })
            }) : angular.forEach(s.documents, function(n) {
                var t = s.inArray(s.allSubjects, n.CoreSubject.Code);
                t || s.allSubjects.push({
                    Code: n.CoreSubject.Code,
                    Name: n.CoreSubject.Name,
                    Checked: !0
                })
            });
            s.allSubjects != undefined && s.allSubjects != null && s.allSubjects.length > 0 && (s.subjectFilterClassData = !0)
        }
        ;
        this.setDocumentAsId = function(n, t, i, r) {
            return n + "-" + t + "-" + i + "-" + r.split(" ").join("").replace("(", "").replace(")", "").replace(".", "").replace(".", "").replace(":", "")
        }
        ;
        this.getWeekName = function(n, t) {
            var i = s.isCurrentWeek(n, t);
            return SDPUtility.getWeekStringName(t, i)
        }
        ;
        this.getSubjectName = function(n) {
            return n.split(",")[1].trim()
        }
        ;
        this.isCurrentWeek = function(n, t) {
            return s.currentTermWeek.Term == n && s.currentTermWeek.TermWeek == t
        }
        ;
        this.setDocumentAsRead = function(n) {
            var r;
            if (n.OnlineQuizObject == null) {
                if (!n.IsRead) {
                    n.IsRead = !0;
                    u.$emit("documentIsRead", s.selectedDoc);
                    var t = e.getGeneralInformationNumber()
                      , f = e.getScheduleAndTimetablesNumber()
                      , i = e.getExamPreparationNumber()
                      , o = e.getGridNumber();
                    switch (s.docCode) {
                    case "1":
                        e.setGeneralInformationNumber(t - 1);
                        break;
                    case "2":
                        e.setGeneralInformationNumber(t - 1);
                        break;
                    case "4":
                        e.setExamPreparationNumber(i - 1);
                        break;
                    case "6":
                        e.setExamPreparationNumber(i - 1);
                        break;
                    case "5":
                        e.setGridNumber(o - 1);
                        break;
                    case "3":
                        e.setScheduleAndTimetablesNumber(f - 1)
                    }
                }
                r = apiUrls.getDownloadUrlAndSetAsRead(n.DownloadDocumentId, n.DocumentSchoolLinkId, s.studentAccountId, s.selectedSchoolId);
                window.open(r)
            } else
                s.loadPopupOnlineQuiz(n.OnlineQuizObject)
        }
        ;
        this.getDocumentUrl = function(n) {
            return apiUrls.getDownloadUrlAndSetAsRead(n.DownloadDocumentId, n.DocumentSchoolLinkId, this.studentAccountId, s.selectedSchoolId)
        }
        ;
        this.filterSelection = function(n) {
            switch (n) {
            case "Term":
                s.termFilter = !s.termFilter;
                s.weekFilter = !1;
                s.subjectFilter = !1;
                s.termFilter ? (s.termFilterClassOpen = !0,
                s.weekFilterClassOpen = !1,
                s.subjectFilterClassOpen = !1) : (s.termFilterClassOpen = !1,
                s.weekFilterClassOpen = !1,
                s.subjectFilterClassOpen = !1);
                break;
            case "Week":
                s.termFilter = !1;
                s.weekFilter = !s.weekFilter;
                s.subjectFilter = !1;
                s.weekFilter ? (s.termFilterClassOpen = !1,
                s.weekFilterClassOpen = !0,
                s.subjectFilterClassOpen = !1) : (s.termFilterClassOpen = !1,
                s.weekFilterClassOpen = !1,
                s.subjectFilterClassOpen = !1);
                break;
            case "Subject":
                s.termFilter = !1;
                s.weekFilter = !1;
                s.subjectFilter = !s.subjectFilter;
                s.subjectFilter ? (s.termFilterClassOpen = !1,
                s.weekFilterClassOpen = !1,
                s.subjectFilterClassOpen = !0) : (s.termFilterClassOpen = !1,
                s.weekFilterClassOpen = !1,
                s.subjectFilterClassOpen = !1)
            }
            s.filterDataClass()
        }
        ;
        this.selectTerm = function(n) {
            if (s.selectedTerms = [],
            n === 0) {
                if (s.selectAllTerms)
                    angular.forEach(s.allTerms, function(n) {
                        n.Checked = !0;
                        s.selectedTerms.push(n.Term)
                    });
                else if (angular.forEach(s.allTerms, function(n) {
                    n.Checked = !1
                }),
                s.allWeeks = [],
                s.selectedWeeks = [],
                s.arrSelectedWeeksDescription = [],
                s.GetSelectedWeeksLabel(),
                s.docCode != 4) {
                    s.loadFilterData(s.readUnreadDocuments);
                    return
                }
            } else {
                var t = !0;
                angular.forEach(s.allTerms, function(n) {
                    n.Checked ? s.selectedTerms.push(n.Term) : (t = !1,
                    s.selectAllTerms = !1)
                });
                t && (s.selectAllTerms = !0)
            }
            s.selectedTerms != undefined && s.selectedTerms != null && s.selectedTerms.length > 0 ? s.docCode == 4 ? s.loadAllWeeksPerTerms(s.selectedSchoolId, s.selectedTerms, s.currentTermWeek.TermWeek, !1, function() {
                s.loadAMSQuiz(!1)
            }) : s.loadAllWeeksPerTerms(s.selectedSchoolId, s.selectedTerms, s.currentTermWeek.TermWeek, !1) : s.docCode == 4 && s.loadFilterData(s.readUnreadDocuments)
        }
        ;
        this.loadAllWeeksPerTerms = function(t, i, r, u, f) {
            var e = !1;
            s.selectAllWeeks = !1;
            s.allWeeks = [];
            s.selectedWeeks = [];
            s.arrSelectedWeeksDescription = [];
            s.GetSelectedWeeksLabel();
            n.loadAllWeeksPerTerms(t, i).then(function(n) {
                if (SDPUtility.isDefined(n.data)) {
                    angular.forEach(n.data, function(t) {
                        if (n.data.length > 0) {
                            u ? (e = !1,
                            t.TermWeek === r && (s.weekFilterClassData = !0,
                            e = !0,
                            s.selectedWeeks.indexOf(t.TermWeek) == -1 && (s.selectedWeeks.push(t.TermWeek),
                            s.arrSelectedWeeksDescription.push(t.Description),
                            s.GetSelectedWeeksLabel()))) : (s.selectAllWeeks = !0,
                            s.selectedWeeks.push(t.TermWeek),
                            s.arrSelectedWeeksDescription = [],
                            s.GetSelectedWeeksLabel(),
                            e = !0);
                            var i = s.inArrayWeek(s.allWeeks, t.Description);
                            i || s.allWeeks.push({
                                Term: t.Term,
                                Week: t.TermWeek,
                                WeekDescription: t.Description,
                                Checked: e,
                                IsSummerWeek: t.IsSummerWeek
                            })
                        }
                    });
                    var t = SDPUtility.groupArrayBy(s.allWeeks, function(n) {
                        return [n.IsSummerWeek]
                    }), i;
                    t != undefined && t != null && (t.length > 1 ? (i = t[0].concat(t[1]),
                    s.allWeeks = i.slice(0)) : t != undefined && t != null && (i = t[0],
                    s.allWeeks = i.slice(0)));
                    f != null && typeof f == "function" ? f() : (s.loadAllSubjects(),
                    s.loadFilterData(s.readUnreadDocuments))
                }
            })
        }
        ;
        this.selectWeek = function(n) {
            if (s.selectedWeeks = [],
            s.arrSelectedWeeksDescription = [],
            s.GetSelectedWeeksLabel(),
            n === 1) {
                if (s.selectAllWeeks)
                    angular.forEach(s.allWeeks, function(n) {
                        n.Checked = !0;
                        s.selectedWeeks.push(n.Week)
                    });
                else if (angular.forEach(s.allWeeks, function(n) {
                    n.Checked = !1
                }),
                s.docCode != 4) {
                    s.loadFilterData(s.readUnreadDocuments);
                    return
                }
            } else {
                var t = !0;
                angular.forEach(s.allWeeks, function(n) {
                    n.Checked ? (s.selectedWeeks.push(n.Week),
                    s.arrSelectedWeeksDescription.push(n.WeekDescription),
                    s.GetSelectedWeeksLabel()) : (t = !1,
                    s.selectAllWeeks = !1)
                });
                t && (s.selectAllWeeks = !0)
            }
            s.docCode == 4 ? s.loadAMSQuiz(!1) : s.loadFilterData(s.readUnreadDocuments)
        }
        ;
        this.GetSelectedWeeksLabel = function() {
            var n = ""
              , i = []
              , t = [];
            angular.forEach(s.arrSelectedWeeksDescription, function(n) {
                var u = n.split(" ")
                  , r = u[u.length - 1];
                t.includes(n.replace(r, "")) || t.push(n.replace(r, ""));
                i.push({
                    WeekDescription: n,
                    prefix: n.replace(r, ""),
                    suffix: r
                })
            });
            angular.forEach(t, function(t) {
                n != "" && (n += ", ");
                n += t;
                var r = 0;
                angular.forEach(i, function(i) {
                    i.prefix == t && (r != 0 && (n += ", "),
                    n += i.suffix,
                    r++)
                })
            });
            s.selectedWeeksLabel = n
        }
        ;
        this.selectSubject = function(n) {
            if (n === 1) {
                if (!s.selectAllSubjects) {
                    angular.forEach(s.allSubjects, function(n) {
                        n.Checked = !1
                    });
                    s.loadFilterData(s.readUnreadDocuments);
                    return
                }
                angular.forEach(s.allSubjects, function(n) {
                    n.Checked = !0
                })
            } else {
                var t = !0;
                angular.forEach(s.allSubjects, function(n) {
                    n.Checked || (t = !1,
                    s.selectAllSubjects = !1)
                });
                t && (s.selectAllSubjects = !0)
            }
            s.loadFilterData(s.readUnreadDocuments)
        }
        ;
        this.inArray = function(n, t) {
            var i = !1;
            return angular.forEach(n, function(n) {
                i || n.Code !== t || (i = !0)
            }),
            i
        }
        ;
        this.inArrayWeek = function(n, t) {
            var i = !1;
            return angular.forEach(n, function(n) {
                i || n.WeekDescription !== t || (i = !0)
            }),
            i
        }
        ;
        this.loadFilterData = function(n) {
            s.documentsFound = !1;
            angular.forEach(s.documents, function(t) {
                t.Display = !1;
                s.docCode == 8 ? angular.forEach(s.allSubjects, function(i) {
                    if (i.Checked) {
                        var r = "";
                        r = s.docCode != "-99" ? t.SubSubject.Subject.Code : t.CoreSubject.Code;
                        r === i.Code && (n !== undefined && n == !0 ? !t.IsRead === n && (t.Display = !0) : t.Display = !0)
                    }
                }) : angular.forEach(s.allTerms, function(i) {
                    i.Checked && t.TermWeek.Term === i.Term && (s.documentsFound = !0,
                    angular.forEach(s.allWeeks, function(i) {
                        i.Checked && (t.TermWeek.WeekDescriptionValue === i.WeekDescription || t.TermWeek.WeekNumber === 0 || s.docCode == -99 && t.TermWeek.WeekNumber === 99) && angular.forEach(s.allSubjects, function(i) {
                            if (i.Checked) {
                                var r = "";
                                r = s.docCode != "-99" ? t.SubSubject.Subject.Code : t.CoreSubject.Code;
                                r === i.Code && (n !== undefined && n == !0 ? !t.IsRead === n && (t.Display = !0) : t.Display = !0)
                            }
                        })
                    }))
                })
            });
            s.showFilter();
            s.isLoading = !1
        }
        ;
        this.containsSelection = function(n) {
            var t = !1;
            return angular.forEach(n, function(n) {
                n.Checked && (t = !0)
            }),
            t
        }
        ;
        this.filterDataClass = function() {
            s.termFilterClassData = s.containsSelection(s.allTerms) ? !0 : !1;
            s.weekFilterClassData = s.containsSelection(s.allWeeks) ? !0 : !1;
            s.subjectFilterClassData = s.containsSelection(s.allSubjects) ? !0 : !1
        }
        ;
        this.viewUnreadDocuments = function() {
            s.readUnreadDocuments = !s.readUnreadDocuments;
            s.termFilter = !1;
            s.weekFilter = !1;
            s.subjectFilter = !1;
            s.termFilterClassOpen = !1;
            s.weekFilterClassOpen = !1;
            s.subjectFilterClassOpen = !1;
            s.readUnreadDocuments ? (s.viewUnreadDocumentsLabel = "View All Documents",
            s.loadFilterData(s.readUnreadDocuments)) : (s.viewUnreadDocumentsLabel = "View Unread Documents",
            s.loadFilterData(s.readUnreadDocuments))
        }
        ;
        this.viewCurrentTermWeek = function() {
            s.selectCurrentTermWeek = !s.selectCurrentTermWeek;
            s.selectedDoc !== "-1" && s.studentAccountId !== "-1" && (s.resetVariables(),
            s.loadDocuments(s.docId, s.studentAccountId, s.acadYear, !0))
        }
        ;
        this.resetVariables = function() {
            s.allTerms = [];
            s.allWeeks = [];
            s.allSubjects = [];
            s.textToHighlight = "";
            s.documents = [];
            s.currentTermWeek = null;
            s.selectedTerms = [];
            s.selectedWeeks = [];
            s.termFilter = !1;
            s.weekFilter = !1;
            s.subjectFilter = !1;
            s.selectAllTerms = !1;
            s.selectAllWeeks = !1;
            s.selectAllSubjects = !0;
            s.termFilterClassOpen = !1;
            s.termFilterClassData = !0;
            s.weekFilterClassOpen = !1;
            s.weekFilterClassData = !0;
            s.subjectFilterClassOpen = !1;
            s.subjectFilterClassData = !0;
            s.readUnreadDocuments = !1;
            s.selectCurrentTermWeek = !1;
            s.hideFilterOptions = !1;
            s.hideFilterDocumentsOptions = !1;
            s.isLoading = !0;
            s.viewUnreadDocumentsLabel = "View Unread Documents"
        }
        ;
        this.practiceSession = function(n) {
            var i, r;
            if (n.IsRead) {
                n.IsPracticed = !0;
                n.IsRead = !0;
                u.$emit("documentIsRead", s.selectedDoc);
                i = e.getGridNumber();
                switch (s.selectedDoc) {
                case "-99":
                    e.setGridNumber(i - 1)
                }
            }
            r = window.open();
            t.get(this.getPracticeSessionUrl(n)).then(function(n) {
                r.location = n.data
            })
        }
        ;
        this.canAttemptAMSQuiz = function(n) {
            return apiUrls.canAttemptAMSQuiz(s.studentAccountId, n)
        }
        ;
        this.getAvailabilityDate = function(n, t) {
            return apiUrls.getAvailabilityDate(n, t)
        }
        ;
        this.canAttemptPeriodicQuiz = function(n) {
            var t = "";
            return s.selectedSections = [],
            s.getSelectedSections(n),
            s.selectedSections != null && s.selectedSections.length > 0 && angular.forEach(s.selectedSections, function(n) {
                t != "" && (t += ",");
                t += n.PKForSync
            }),
            apiUrls.canAttemptPeriodicQuiz(s.studentAccountId, n)
        }
        ;
        this.getPracticeSessionUrl = function(n) {
            return apiUrls.getPracticeSessionPath(n.PrepListSessionId, n.ContentTypeId, s.studentAccountId)
        }
        ;
        this.hideFilter = function() {
            u.$emit("mobileFilterSelected", "row-filter-mobile")
        }
        ;
        this.slideRight = function() {
            var t = $(".DocumentList")
              , n = $(".DocumentList").scrollLeft() + 200
              , i = t[0].scrollWidth - t[0].clientWidth;
            n > i && (n = i);
            $(".DocumentList").animate({
                scrollLeft: n
            }, 800);
            setTimeout(function() {
                s.ControlTabsNavigationButtons()
            }, 900)
        }
        ;
        this.slideLeft = function() {
            var n = $(".DocumentList").scrollLeft();
            $(".DocumentList").animate({
                scrollLeft: n - 200
            }, 800);
            setTimeout(function() {
                s.ControlTabsNavigationButtons()
            }, 900)
        }
        ;
        this.ControlTabsNavigationButtons = function() {
            var n = $(".DocumentList")
              , t = $(".previous-tabs")
              , i = $(".next-tabs");
            n[0].scrollLeft == 0 ? t.hide() : t.show();
            n[0].scrollLeft == n[0].scrollWidth - n[0].clientWidth ? i.hide() : i.show()
        }
        ;
        this.loadPopupOnlineQuiz = function(n) {
            s.viewHistoryCheckbox = "viewHistoryRdb";
            s.newQuizCheckbox = "newQuiz";
            var i = !0;
            s.docCode == 8 ? t.get(this.canAttemptPeriodicQuiz(n.ID)).then(function(t) {
                var f = !1
                  , r = !1;
                t.data != null && t.data.length > 0 && (t.data[0].SessionQuizId != null && t.data[0].SessionQuizId != "BC3djp%2F56bY%3D" ? (n.SessionQuizId = t.data[0].SessionQuizId,
                r = !0) : (r = !1,
                t.data[0].IsSubmitted = !0),
                f = !0 && (t.data[0].RemainingSessions == -1 || t.data[0].RemainingSessions > 0) ? !0 : !1);
                !n.QuizAvailability.HasHistory && (f || r) && (s.viewHistoryCheckbox = "newQuizCheckRdb");
                f ? s.newQuizCheckbox = "newQuiz" : r && (s.newQuizCheckbox = "resumeQuiz");
                s.popupOnlineQuizModelCenter = {
                    StartDate: GetPopupDate(n.QuizAvailability.QuizStart),
                    EndDate: GetPopupDate(n.QuizAvailability.QuizEnd),
                    isEnded: n.QuizAvailability.QuizEnd.substring(0, 10) != "0001-01-01" && GetUTCDate() > new Date(n.QuizAvailability.QuizEnd),
                    title: "Start",
                    popupId: n.ID,
                    popupQuizLevelSectionId: n.QuizLevelSection.ID,
                    popupSessionQuizId: n.SessionQuizId,
                    isReadOnly: n.QuizAvailability.IsDeleted,
                    hasHistory: n.QuizAvailability.HasHistory,
                    isUnfinished: n.QuizAvailability.IsUnfinished,
                    isSubmitted: t.data[0].IsSubmitted,
                    isRetake: n.SessionQuiz.Status,
                    isDeleted: n.QuizAvailability.IsDeleted,
                    historyDescription: "View History",
                    attemptDescription: "Attempt Quiz",
                    startNewDescription: "Start New Quiz",
                    resumeDescription: "Resume Quiz",
                    retakeDescription: "Attempt Incorrect Questions Again",
                    canAttemptAMSQuiz: f,
                    retakeOptions: n.RetakeOptions,
                    durationDay: n.DurationDay,
                    durationHour: n.DurationHour,
                    durationMin: n.DurationMin,
                    sessionStartTime: n.SessionQuiz.StartDate,
                    isAllowed: i,
                    AllowedAttempts: t.data[0].AllowedNumberOfAttempts,
                    Description: n.Description,
                    canResumeAMSQuiz: r
                };
                s.isActive = !1;
                s.isActive = s.popupOnlineQuizModelCenter.hasHistory != 1 && s.popupOnlineQuizModelCenter.isDeleted == 1 ? !1 : !0;
                n.QuizAvailability.IsDeleted ? $("#popupOnlineQuizDialog").modal("show") : (!n.QuizAvailability.IsDeleted || n.QuizAvailability.HasHistory) && (u.studentTypeId == 3 || n.QuizAvailability.HasHistory) && $("#popupOnlineQuizDialog").modal("show");
                $(":focus").blur()
            }) : t.get(this.canAttemptAMSQuiz(n.ID)).then(function(t) {
                var f = !1
                  , e = 0
                  , r = !1;
                e = n.QuizAvailability.IsDeleted;
                t.data != null && t.data.length > 0 && (t.data[0].SessionQuizId != null && t.data[0].SessionQuizId != "BC3djp%2F56bY%3D" ? (n.SessionQuizId = t.data[0].SessionQuizId,
                r = !0) : (r = !1,
                t.data[0].IsSubmitted = !0),
                f = n.QuizAvailability.IsDeleted == 0 && (t.data[0].RemainingSessions == -1 || t.data[0].RemainingSessions > 0) ? !0 : !1);
                !n.QuizAvailability.HasHistory && (f || r) && (s.viewHistoryCheckbox = "newQuizCheckRdb");
                f ? s.newQuizCheckbox = "newQuiz" : r && (s.newQuizCheckbox = "resumeQuiz");
                s.popupOnlineQuizModelCenter = {
                    StartDate: GetPopupDate(n.QuizAvailability.QuizStart),
                    EndDate: GetPopupDate(n.QuizAvailability.QuizEnd),
                    isEnded: n.QuizAvailability.QuizEnd.substring(0, 10) != "0001-01-01" && GetUTCDate() > new Date(n.QuizAvailability.QuizEnd),
                    title: "Start",
                    popupId: n.ID,
                    popupQuizLevelSectionId: n.QuizLevelSection.ID,
                    popupSessionQuizId: n.SessionQuizId,
                    isReadOnly: n.QuizAvailability.IsDeleted,
                    hasHistory: n.QuizAvailability.HasHistory,
                    isUnfinished: n.QuizAvailability.IsUnfinished,
                    isSubmitted: t.data[0].IsSubmitted,
                    isRetake: n.SessionQuiz.Status,
                    isDeleted: n.QuizAvailability.IsDeleted,
                    historyDescription: "View History",
                    attemptDescription: "Attempt Quiz",
                    startNewDescription: "Start New Quiz",
                    resumeDescription: "Resume Quiz",
                    retakeDescription: "Attempt Incorrect Questions Again",
                    canAttemptAMSQuiz: f,
                    retakeOptions: n.RetakeOptions,
                    durationDay: n.DurationDay,
                    durationHour: n.DurationHour,
                    durationMin: n.DurationMin,
                    sessionStartTime: n.SessionQuiz.StartDate,
                    isAllowed: i,
                    AllowedAttempts: t.data[0].AllowedNumberOfAttempts,
                    Description: n.Description,
                    canResumeAMSQuiz: r,
                    QuizCourseId: n.QuizAvailability.QuizCourseId,
                    QuizCourseGroupId: n.QuizAvailability.QuizCourseGroupId
                };
                s.isActive = !1;
                s.isActive = s.popupOnlineQuizModelCenter.hasHistory != 1 && s.popupOnlineQuizModelCenter.isDeleted == 1 ? !1 : !0;
                n.QuizAvailability.IsDeleted ? $("#popupOnlineQuizDialog").modal("show") : (!n.QuizAvailability.IsDeleted || n.QuizAvailability.HasHistory) && (u.studentTypeId == 3 || n.QuizAvailability.HasHistory) && $("#popupOnlineQuizDialog").modal("show");
                $(":focus").blur()
            })
        }
        ;
        this.loadQuizSession = function(t) {
            var i = "";
            s.viewHistoryCheckbox === "viewHistoryRdb" && t.hasHistory ? window.location.href = s.docCode == 8 ? PublicVariables.MenuItemUrl.NavigateQuizResult + "quizId=" + t.popupId + "&isDeleted=" + t.isDeleted + "&quizLevelSectionId=" + t.popupQuizLevelSectionId + "&accountId=" + s.studentAccountId + "&selectedQuizSessionId=" + t.popupSessionQuizId + "&scid=" + s.selectedSchoolId + "&sessionType=3" : PublicVariables.MenuItemUrl.NavigateQuizResult + "quizId=" + t.popupId + "&isDeleted=" + t.isDeleted + "&quizLevelSectionId=" + t.popupQuizLevelSectionId + "&accountId=" + s.studentAccountId + "&selectedQuizSessionId=" + t.popupSessionQuizId + "&scid=" + s.selectedSchoolId : s.viewHistoryCheckbox === "newQuizCheckRdb" && (i = PublicVariables.MenuItemUrl.NavigateOnlineQuiz + PublicVariables.Constants.QueryStringKeys.OnlineQuizId + "=" + t.popupId + "&quizLevelSectionId=" + t.popupQuizLevelSectionId + "&" + PublicVariables.Constants.QueryStringKeys.PageSchoolId + "=" + s.selectedSchoolId + "&accountId=" + s.studentAccountId,
            s.newQuizCheckbox === "newQuiz" ? s.docCode == 8 ? (i = PublicVariables.MenuItemUrl.NavigateOnlineQuiz + PublicVariables.Constants.QueryStringKeys.OnlineQuizId + "=" + t.popupId + "&" + PublicVariables.Constants.QueryStringKeys.PageSchoolId + "=" + s.selectedSchoolId + "&accountId=" + s.studentAccountId,
            n.createPeriodicSession(t.popupId, s.selectedSections, t.QuizCourseId, t.QuizCourseGroupId).then(function(n) {
                if (n.data.IsSessionLocked) {
                    alert("This session has expired.\r\nYou will be logged out. Please Login again.");
                    window.location = "/Logout.aspx";
                    return
                }
                s.validateSessionStart(n.data.SessionId) && (window.location.href = i + "&sessionId=" + n.data.SessionId + "&sessionType=3")
            })) : n.createSession(t.popupId, t.popupQuizLevelSectionId, s.studentAccountId, t.QuizCourseId, t.QuizCourseGroupId).then(function(n) {
                if (n.data.IsSessionLocked) {
                    alert("This session has expired.\r\nYou will be logged out. Please Login again.");
                    window.location = "/Logout.aspx";
                    return
                }
                s.validateSessionStart(n.data.SessionId) && (window.location.href = i + "&sessionId=" + n.data.SessionId)
            }) : s.newQuizCheckbox === "resumeQuiz" ? n.checkSessionLockStatus(t.popupId).then(function(r) {
                if (r.data) {
                    alert("This session has expired.\r\nYou will be logged out. Please Login again.");
                    window.location = "/Logout.aspx";
                    return
                }
                n.checkSessionTimePassed(t.popupId, t.popupSessionQuizId, t.QuizCourseId, t.QuizCourseGroupId).then(function(n) {
                    n.data ? (alert("The time allowed for this quiz has ended.\n The quiz will be submitted automatically."),
                    s.resetVariables(),
                    s.loadDocuments(s.docId, s.studentAccountId, s.acadYear, !1)) : s.docCode == 8 ? (i = PublicVariables.MenuItemUrl.NavigateOnlineQuiz + PublicVariables.Constants.QueryStringKeys.OnlineQuizId + "=" + t.popupId + "&" + PublicVariables.Constants.QueryStringKeys.PageSchoolId + "=" + s.selectedSchoolId + "&accountId=" + s.studentAccountId,
                    window.location.href = i + "&sessionId=" + t.popupSessionQuizId + "&sessionType=3") : window.location.href = i + "&sessionId=" + t.popupSessionQuizId
                }, function(n) {
                    s.handleErrorResponse(n)
                })
            }) : s.newQuizCheckbox === "retakeQuiz" && n.checkSessionLockStatus(t.popupId).then(function(r) {
                if (r.data) {
                    alert("This session has expired.\r\nYou will be logged out. Please Login again.");
                    window.location = "/Logout.aspx";
                    return
                }
                n.checkSessionTimePassed(t.popupId, t.popupSessionQuizId, t.QuizCourseId, t.QuizCourseGroupId).then(function(r) {
                    r.data ? (alert("The time allowed for this quiz has ended.\n The quiz will be submitted automatically."),
                    s.resetVariables(),
                    s.loadDocuments(s.docId, s.studentAccountId, s.acadYear, !1)) : n.saveQuizSession(t.popupSessionQuizId, "3", t.isRetake).then(function() {
                        s.docCode == 8 ? (i = PublicVariables.MenuItemUrl.NavigateOnlineQuiz + PublicVariables.Constants.QueryStringKeys.OnlineQuizId + "=" + t.popupId + "&" + PublicVariables.Constants.QueryStringKeys.PageSchoolId + "=" + s.selectedSchoolId + "&accountId=" + s.studentAccountId,
                        window.location.href = i + "&sessionId=" + t.popupSessionQuizId + "&sessionType=3") : window.location.href = i + "&sessionId=" + t.popupSessionQuizId
                    }, function(n) {
                        s.handleErrorResponse(n)
                    })
                }, function(n) {
                    s.handleErrorResponse(n)
                })
            }))
        }
        ;
        this.handleErrorResponse = function(n) {
            if (n.data && n.data.Code) {
                let t = SDPResources[n.data.Code];
                alert(t);
                window.location.reload()
            } else
                SDPUtility.handleErrorResponse(n)
        }
        ;
        this.validateSessionStart = function(n) {
            var t = n.toLowerCase() != s.maxAttemptsExeededId.toLowerCase();
            return t || (alert("You have exeeded the allowed number of attempts."),
            window.location.reload()),
            t
        }
        ;
        this.selectBook = function(n) {
            n != null && n.Chapter != null && n.Chapter.length > 0 && angular.forEach(n.Chapter, function(t) {
                t.Checked = n.Checked;
                s.selectChapter(t)
            })
        }
        ;
        this.selectChapter = function(n, t) {
            n != null && n.Section != null && n.Section.length > 0 && angular.forEach(n.Section, function(t) {
                t.Checked = n.Checked
            });
            var i = !0;
            t != null && t.Chapter.length > 0 && (angular.forEach(t.Chapter, function(n) {
                n.Checked != !0 && (i = !1)
            }),
            t.Checked = i)
        }
        ;
        this.selectSection = function(n, t) {
            var r = !0, i;
            n != null && n.Section != null && n.Section.length > 0 && (angular.forEach(n.Section, function(n) {
                n.Checked != !0 && (r = !1)
            }),
            n.Checked = r,
            i = !0,
            t != null && t.Chapter.length > 0 && (angular.forEach(t.Chapter, function(n) {
                n.Checked != !0 && (i = !1)
            }),
            t.Checked = i))
        }
        ;
        this.getSelectedSections = function(n) {
            var t = s.documents.filter(t=>t.OnlineQuizObject.ID == n);
            t != null && t.length > 0 && t[0].Book != null && t[0].Book.length > 0 && angular.forEach(t[0].Book, function(n) {
                n.Chapter != null && n.Chapter.length > 0 && angular.forEach(n.Chapter, function(n) {
                    n.Section != null && n.Section.length > 0 && angular.forEach(n.Section, function(n) {
                        n != null && n.Checked && s.selectedSections.push(n)
                    })
                })
            })
        }
        ;
        this.initialize()
    }
    ])
}
)();
GetPopupDate = function(n) {
    if (n != "0001-01-01T00:00:00") {
        var t = (new Date).getTimezoneOffset();
        dt = new Date(new Date(n).getTime() + -6e4 * t);
        return ("0" + dt.getDate()).slice(-2) + "-" + ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][dt.getMonth()] + "-" + ("0" + dt.getFullYear()).slice(-4) + " " + ("0" + dt.getHours()).slice(-2) + ":" + ("0" + dt.getMinutes()).slice(-2)
    }
    return "01-January-01"
}
;
GetUTCDate = function() {
    var n = new Date;
    return new Date(n.getUTCFullYear(),n.getUTCMonth(),n.getUTCDate(),n.getUTCHours(),n.getUTCMinutes(),n.getUTCSeconds())
}
;
